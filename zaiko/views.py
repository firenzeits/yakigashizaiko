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
    date_format = datetime(2019,1,1,0,0,0,tzinfo=utc)
    recent_date = ["最終更新日時",date_format,date_format,date_format,date_format,date_format,date_format,date_format,date_format,"---"]
    recent=date_format
    
    data = StockStatus.objects.all().values_list('item','shop','num','update_date')
    itemlist = Item.objects.all().values_list('item')
    shoplist = Shop.objects.all().values_list('shop')

    #商品,高畑num,かの里num,岩塚num,大治num,マエストロnum,クオレnum,ラボ3,ラボ2,合計
    #の２次元配列を作る。
    itemnum = len(itemlist)
    arr = [[0 for i in range(10)] for j in range(itemnum)]  #2次元配列初期化
    
    #配列に品名をセット
    for i in range(itemnum):                #商品名分ループ
        arr[i][0] = itemlist[i][0]      #列名に商品名をセット

        for j in data:                  #在庫TBLのレコードを１行ずつ読む。商品名,店名,数量
           arr[j[0]-1][j[1]] = j[2]     #j[0]は商品TBLのID（１はじまり。）、j[1]はユーザID（店名）,j[2]は数量。

           if ( recent_date[j[1]] < j[3]):
               recent_date[j[1]] = j[3]

        zaikototal = 0
        shopnum = len(shoplist)         #shopnumは8（フィレンツェ４＋マエストロ＋クオレ＋ラボ２、３
        for l in range(shopnum):        #rangeは長さshopnumのリストを作る。（8なら、{0,1,2,3,4,5,6,7}
            zaikototal += arr[i][l+1]   #0は商品名なので、＋1

        arr[i][shopnum + 1] = zaikototal

                
        
            
    params = {
            'title':'在庫管理システム',
            'data':arr,
            'recentdate':recent_date,
            }
    return render(request, 'zaiko/index.html', params)

def update(request,shopid):
    data = []
    recent_date = datetime(2019,1,1,0,0,0,tzinfo=utc)
    
    shopname = Shop.objects.get(id=shopid)
    zaikolist = StockStatus.objects.filter(shop=shopid).values_list('item','num','id','update_date')
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
    meisai=[]
    if (request.method =='POST'):
        obj = ShippingOrder()
        itemobj = Item
        #temp = request.POST
        shippingOrder = ShippingOrderForm(request.POST, instance=obj)
        fromshopid = request.POST['fromshop']
        toshopid = request.POST['toshop']
        itemid = request.POST['item']
        fromshop = Shop(fromshopid)
        toshop = Shop(toshopid)
        item = Item.objects.get(id=itemid)
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
            data.append([str(Shop.objects.get(id=fromshopid)),"→",str(Shop.objects.get(id=toshopid))])
            data.append([fromnum,shippingnum,tonum])
            data.append(["↓ (-"+ shippingnum +")","","↓ (+"+ shippingnum +")"])
            data.append([int(fromnum) - int(shippingnum),"",int(tonum) + int(shippingnum)])

            meisai.append(["品名","数量","単価","金額"])
            meisai.append([str(item.item),int(item.price),int(shippingnum),int(shippingnum) * int(item.price)])
            if shippingOrder.is_valid():
                shippingOrder.save()
            params = {
                    'title':'出荷：在庫管理システム',
                    'form':ShippingOrderForm,
                    'msg':msg,
                    'result':data,
                    'meisai':meisai,
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
    
    