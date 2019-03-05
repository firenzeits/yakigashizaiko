from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db.models import QuerySet
from .models import Item,StockStatus,Shop,ShippingOrder
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .forms import StockStatusForm,ShippingOrderForm,ShippingHistoryForm,ShippingConfirmForm
from datetime import datetime,timedelta
from pytz import timezone, utc
from django.db.models import Q
from django.db.models import Sum

@login_required(login_url='/admin/login/')
def index(request):
    arr = []
    recent_date=[]
    date_format = datetime(2019,1,1,0,0,0,tzinfo=utc)

    shoplist = Shop.objects.all().order_by('id')
    for n in range(len(shoplist)):
        recent_date.append(date_format)

    arr = []
    user = Shop.objects.get(name=request.user)
    
    #user = "xxx"
    notrecievedorderlist = ""
    notrecievedorderlist = ShippingOrder.objects.filter(toshop=user,recieveFlag=False)
    
    if (request.method =='POST'):
        for norecievedorder in notrecievedorderlist:
            norecievedorder.recieveFlag = True
            norecievedorder.save()
            recieve(norecievedorder)
        return redirect(to='index')
    
    for item in Item.objects.all():
        arrline = [0 for i in range(len(shoplist) + 2)]
        arrline[0] = "<p class=\"text-left py-0 mb-0\">" + str(item) + "</p>"
        total = 0
        n = 1                                               
        for shop in shoplist:
            tempdata = StockStatus.objects.get_or_create(item=item, shop=shop,
                                                         defaults=dict(
                                                                 item=item,
                                                                 shop=shop
                                                                 )
                                                         )

            arrline[n] = "<p class=\"text-right py-0 mb-0\">" + str(tempdata[0].num) + "</p>"
            total += tempdata[0].num
            if recent_date[n-1] <  tempdata[0].update_date:   #最終更新日がより最近だったら更新
                recent_date[n-1] = tempdata[0].update_date
            n += 1
        arrline[n] = "<p class=\"text-right py-0 mb-0\">" + str(total) + "</p>"
        arr.append(arrline)
    
        
        
    
    params = {
            'title':'在庫管理システム',
            'shopdata' : shoplist,
            'notrecieved' : notrecievedorderlist,
            'data':arr,
            'recentdate':recent_date,
            'user':user,
            }
    return render(request, 'zaiko/index.html', params)

@login_required(login_url='/admin/login/')
def update(request,shopid):
    data = []
    recent_date = datetime(2019,1,1,0,0,0,tzinfo=utc)
    
    shopname = Shop.objects.get(id=shopid)
#    zaikolist = StockStatus.objects.filter(shop=shopid).order_by('-update_date').values_list('item','num','id','update_date')
    zaikolist = StockStatus.objects.filter(shop=shopid).values_list('item','num','id','update_date')
    for zaiko in zaikolist:
        itemid=zaiko[0]
        itemname = Item.objects.filter(id=itemid).values_list('item')
        innerdata = []
        innerdata.append(itemname[0][0])    #商品名
        innerdata.append(zaiko[1])          #数量
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

@login_required(login_url='/admin/login/')
def shipping(request):
    msg=""
    data=[]
    if (request.method =='POST'):
        fromshopid = request.POST['fromshop']
        toshopid = request.POST['toshop']
        itemid = request.POST['item']
        shippingnum = request.POST['num']        
        
        fromshop = Shop.objects.get(id=fromshopid)
        toshop = Shop.objects.get(id=toshopid)
        itemobj = Item.objects.get(id=itemid)
        
        item = itemobj.item
        price = itemobj.price
        
        fromstockStatus = StockStatus.objects.get_or_create(item=itemid,shop=fromshop)
        tostockStatus = StockStatus.objects.get_or_create(item=itemid,shop=toshop)
        
        fromnum = fromstockStatus[0].num
        tonum = tostockStatus[0].num
        
        
        totalprice = int(shippingnum)*int(price)
        #totalprice = "XXX"
        obj = ShippingOrder()
        #temp = request.POST
        shippingOrder = ShippingOrderForm(request.POST, instance=obj)
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
#            data.append(["品名:",str(Item.objects.get(id=itemid)),""])
#            data.append([str(Shop.objects.get(id=fromshopid)),"→",str(Shop.objects.get(id=toshopid))])
#            data.append([fromnum,shippingnum,tonum])
#            data.append(["↓ (-"+ shippingnum +")","","↓ (+"+ shippingnum +")"])
#            data.append([int(fromnum) - int(shippingnum),"",int(tonum) + int(shippingnum)])

            #[出荷元、元の在庫、出荷数、出荷後在庫、商品名、出荷数、出荷先店舗、出荷先在庫、出荷数、出荷受取後在庫]

            data = [ str(Shop.objects.get(id=fromshopid)),fromnum,shippingnum,int(fromnum) - int(shippingnum),   \
                         str(item)+'@￥'+str(price),int(shippingnum),totalprice,\
                         str(Shop.objects.get(id=toshopid)),tonum,shippingnum,int(tonum) + int(shippingnum) ]

            #shippingOrder.totalprice = totalprice
            if shippingOrder.is_valid():
                shippingOrder.save()
            #在庫の移動は出荷受取り処理後
            fromstockStatus[0].num = int(fromnum) - int(shippingnum)
            #tostockStatus[0].num = int(tonum) + int(shippingnum)
            fromstockStatus[0].save()
            #tostockStatus[0].save()
    params = {
            'title':'出荷：在庫管理システム',
            'form':ShippingOrderForm,
            'errmsg':msg,
            'result':data,
            }
    return render(request, 'zaiko/shipping.html', params)

@login_required(login_url='/admin/login/')
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
        
        flag = request.POST['recieveFlag']
        if (flag == '1'):
            data = data.filter(recieveFlag=False)
        elif (flag == '2'):
            data = data.filter(recieveFlag=True)
        
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
    
    
@login_required(login_url='/admin/login/')
def shippingconfirm(request,shippingid):
    msg = ""

    data = ShippingOrder.objects.get(id=shippingid)
    form = ShippingConfirmForm({'fromshop': data.fromshop, 'toshop':data.toshop, 'item':data.item, 'num':data.num, 'recieveFlag':data.recieveFlag})
    flag = data.recieveFlag
    
    if (request.method =='POST'):
        form = ShippingConfirmForm(request.POST, instance=data)
        form.save()
        afterflag = bool(request.POST['recieveFlag'])
        if ( flag != afterflag and afterflag):
            flag=afterflag
            recieve(data)

    params = {
            'title':'出荷確認：在庫管理システム',
            'id':data.id,
            'date':data.create_date,
            'udate':data.update_date,
            'form':form,
            'errmsg':msg
            }
    return render(request, 'zaiko/shippingconfirm.html', params)

def recieve(data):
    
    toshop = data.toshop
    item = data.item
    num = data.num
    
    stockstatusobj = StockStatus.objects.get_or_create(item=item,shop=toshop)
    stockstatusobj[0].num = int(stockstatusobj[0].num) + int(num)
    stockstatusobj[0].save()


    
    