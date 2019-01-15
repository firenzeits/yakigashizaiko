from django.contrib import admin
from .models import Item,Shop,StockStatus,ShippingOrder

admin.site.register(Item)
admin.site.register(Shop)
admin.site.register(StockStatus)
admin.site.register(ShippingOrder)

