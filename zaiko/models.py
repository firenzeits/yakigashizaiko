from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Itemクラス
class Item(models.Model):
    item = models.CharField(max_length=30)
    price = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.item)
    
    def getItem(self):
        return str(self.item)
    
    def getPrice(self):
        return str(self.price)
        
#Shopクラス
class Shop(models.Model):
    shop = models.CharField(max_length=10)
    name = models.ForeignKey(User, on_delete=models.CASCADE,default=0)
    
    def __str__(self):
        return str(self.shop)
    
    def getId(self):
        return int(self.id)

#stockstatusクラス
class StockStatus(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    shop= models.ForeignKey(Shop, on_delete=models.CASCADE)
    num = models.IntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.shop) + ',' + str(self.item) + ',' + str(self.num)
    
    def getNum(self):
        return(int(self.num))

#shippingOrderクラス
class ShippingOrder(models.Model):
    fromshop = models.ForeignKey(Shop, on_delete=models.CASCADE,related_name = "fromshop")
    toshop = models.ForeignKey(Shop, on_delete=models.CASCADE,related_name = "toshop" )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    num = models.IntegerField(default=0)
    totalprice = models.IntegerField(default=0)
    recieveFlag = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return 'from ' + str(self.fromshop) + ' to ' + str(self.toshop) + ' :' + str(self.item) + ' [' + str(self.num) + '] '