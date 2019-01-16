from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db.models import QuerySet
from .models import Item,StockStatus,Shop,ShippingOrder
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .forms import StockStatusForm,ShippingOrderForm,ShippingHistoryForm
from datetime import datetime,timedelta
from pytz import timezone, utc
from django.db.models import Q
from django.db.models import Sum

def index(request):
    arr = []
    recent_date=[]
    date_format = datetime(2019,1,1,0,0,0,tzinfo=utc)
    
    shoplist = Shop.objects.all().order_by('id').values()
    for n in range(len(shoplist)):
        recent_date.append(date_format)

    arr = []
    for item in Item.objects.all().values():
        arrline = [0 for i in range(len(shoplist) + 2)]
        arrline[0] = item['item']
        total = 0
        n = 1                                               
        for shop in shoplist:
            tempdata = StockStatus.objects.get_or_create(item=item['id'], shop=shop['id'],defaults=dict(item=Item.objects.get(id=item['id']),shop=Shop.objects.get(id=shop['id'])))

            arrline[n] = tempdata[0].num
            total += arrline[n]
            if recent_date[n-1] <  tempdata[0].update_date:   #最終更新日がより最近だったら更新
                recent_date[n-1] = tempdata[0].update_date
            n += 1
        arrline[n] = total
        arr.append(arrline)
    
    params = {
            'title':'在庫管理システム',
            'shopdata' : shoplist,       
            'data':arr,
            'recentdate':recent_date,
            }
    return render(request, 'zaiko/index.html', params)

def update(request,shopid):
    data = []
    recent_date = datetime(2019,1,1,0,0,0,tzinfo=utc)
    
    shopname = Shop.objects.get(id=shopid)
    zaikolist = StockStatus.objects.filter(shop=shopid).order_by('-update_date').values_list('item','num','id','update_date')
    for zaiko in zaikolist:
        itemid=zaiko[0]
        itemname = Item.objects.filter(id=itemid).values_list('item')
        innerdata = []
        innerdata.append(itemname[0][0])    #商品名
        innerdata.append(zaiko[1])          #数量
#        innerdata.append(zaiko[2])          
        innerdata.append(zaiko[3])          #更新日時
        if ( zaiko[3] > recent_date):
            recent_date = zaiko[3]
            
        data.append(innerdata)
        innerdata.clear
    params = {
            'title':'更新：在庫管理システム',
            'shopid':shopid,
            'shopname':shopname,
            'data':data,
            'form':StockStatusForm,
            'recentupdate':recent_date,
            }
    
    if( request.method == 'POST'):
        
        item = Item(request.POST['item'])   #request.POST['item']で取得するのはid(formはModelChoiceField)
        shop = Shop(shopid)
        num = request.POST['num']       
        stockStatus = StockStatus.objects.get_or_create(item=item,shop=shop)
        stockStatus[0].num = num       
        stockStatus[0].save()
        url='/zaiko/update/' + str(shopid)
        return redirect(to=url)

    return render(request, 'zaiko/update.html', params)

def shipping(request):
    msg=""
    data=[]
    if (request.method =='POST'):
        obj = ShippingOrder()
        #temp = request.POST
        shippingOrder = ShippingOrderForm(request.POST, instance=obj)
        fromshopid = request.POST['fromshop']
        toshopid = request.POST['toshop']
        itemid = request.POST['item']
        fromshop = Shop(fromshopid)
        toshop = Shop(toshopid)
#        item = Item.objects.get(id=itemid)
        item = Item(itemid) 
        shippingnum = request.POST['num']        
        fromstockStatus = StockStatus.objects.get_or_create(item=item,shop=fromshop)
        tostockStatus = StockStatus.objects.get_or_create(item=item,shop=toshop)
        fromnum = fromstockStatus[0].num
        tonum = tostockStatus[0].num
        if ( int(fromnum) < int(shippingnum) ):
            msg="在庫数が出荷数より少ないです。"
            params = {
                    'title':'出荷：在庫管理システム',
                    'form':ShippingOrderForm,
                    'msg':msg,
                    'result':data,
                    }
            return render(request, 'zaiko/shipping.html', params)
        else:
            msg="以下の通り在庫を移動させます。"
            data.append(["品名:",str(Item.objects.get(id=itemid)),""])
            data.append([str(Shop.objects.get(id=fromshopid)),"→",str(Shop.objects.get(id=toshopid))])
            data.append([fromnum,shippingnum,tonum])
            data.append(["↓ (-"+ shippingnum +")","","↓ (+"+ shippingnum +")"])
            data.append([int(fromnum) - int(shippingnum),"",int(tonum) + int(shippingnum)])

            if shippingOrder.is_valid():
                shippingOrder.save()
            params = {
                    'title':'出荷：在庫管理システム',
                    'form':ShippingOrderForm,
                    'msg':msg,
                    'result':data,
                    }
            fromstockStatus[0].num = int(fromnum) - int(shippingnum)
            tostockStatus[0].num = int(tonum) + int(shippingnum)
            fromstockStatus[0].save()
            tostockStatus[0].save()
        return render(request, 'zaiko/shipping.html', params)
    params = {
            'title':'出荷：在庫管理システム',
            'form':ShippingOrderForm,
            'errmsg':msg
            }
    return render(request, 'zaiko/shipping.html', params)

def shippinghistory(request):
    msg = ""
    data = ShippingOrder.objects.all().order_by('-create_date')

    if ( request.method == 'POST'):
        msg = ""
        fromshop = request.POST['fromshop']
        if (fromshop != ''):
            data = data.filter(fromshop=fromshop)
            msg += "出荷元：" + str(Shop.objects.get(id=fromshop)) + ", "
        toshop= request.POST['toshop']
        if (toshop != ''):
            data = data.filter(toshop=toshop)
            msg += "出荷先：" + str(Shop.objects.get(id=toshop)) + ", "
        item = request.POST['item']
        if (item != ''):
            data = data.filter(item=item)
            msg += "商品：" + str(Item.objects.get(id=item)) + ", "
        
        start = request.POST['start']
        end = request.POST['end']
        if ( start != '' and end != '' ):
            startdate = datetime.strptime(start, '%Y-%m-%d')        
            enddate = datetime.strptime(end, '%Y-%m-%d')
            enddate = enddate + timedelta(days=1)               #検索範囲の終わり（たとえば1月4日までの場合）は、1月4日の分も含めたいので、1日増やした日にちにする。         
            data = data.filter(update_date__range=[startdate, enddate])
            msg += start + "から" + end + "まで"
        elif ( start == '' and end != '' ):
            enddate = datetime.strptime(end, '%Y-%m-%d')
            enddate = enddate + timedelta(days=1)               #検索範囲の終わり（たとえば1月4日までの場合）は、1月4日の分も含めたいので、1日増やした日にちにする。         
            data = data.filter(update_date__lte=enddate)   
            msg += end + "まで"
        elif ( start != '' and end == '' ):
            startdate = datetime.strptime(start, '%Y-%m-%d')       
            data = data.filter(update_date__gte=startdate)
            msg += start + "から"
            
    if (msg == ""):
        msg = "すべて"
        
    total = data.aggregate(Sum('num'))
            
    params = {
            'title':"出荷履歴",
            'form':ShippingHistoryForm,
            'data':data,
            'msg':msg,
            'count':data.count(),
            'sum':total['num__sum'],
            }
    
    
    return render(request, 'zaiko/shippinghistory.html', params)
    
    