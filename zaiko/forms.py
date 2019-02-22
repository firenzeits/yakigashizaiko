# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 12:55:17 2018

@author: RYUICHI
"""

from django import forms
from .models import Item,Shop,ShippingOrder

class HelloForm(forms.Form):
    name = forms.CharField(label='name')
    mail = forms.CharField(label='mail')
    age = forms.IntegerField(label='age')
    height = forms.IntegerField(label='height')
    
class StockStatusForm(forms.Form):
    #shop = forms.ModelChoiceField(label='shop',queryset=Shop.objects.all())
    item = forms.ModelChoiceField(label='item',queryset=Item.objects.all())
    #shop = forms.CharField(label='shop')
    #item = forms.CharField(label='item')
    num = forms.IntegerField(label='num')    
    
class ShippingOrderForm(forms.ModelForm):
    fromshop = forms.ModelChoiceField(label='出荷店',queryset=Shop.objects.all())
    toshop = forms.ModelChoiceField(label='出荷先',queryset=Shop.objects.all())
    item = forms.ModelChoiceField(label='商品名',queryset=Item.objects.all())
    num = forms.IntegerField(label='数量')
    #totalprice = forms.IntegerField(label='数量')
    
    class Meta:
        model = ShippingOrder
        fields = [ 'fromshop', 'toshop', 'item', 'num']
        #fields = [ 'fromshop', 'toshop', 'item', 'num', 'totalprice']
    

class ShippingHistoryForm(forms.ModelForm):
    sentakushi = [
            [0, 'すべて'],
            [1, '未受取'],
            [2, '受取済'],
            ]
    fromshop = forms.ModelChoiceField(label='出荷店',queryset=Shop.objects.all(), required=False)
    toshop = forms.ModelChoiceField(label='出荷先',queryset=Shop.objects.all(), required=False)
    item = forms.ModelChoiceField(label='商品名',queryset=Item.objects.all(), required=False)
    start = forms.DateField(label='start', required=False)
    end = forms.DateField(label='end', required=False)
    recieveFlag = forms.ChoiceField(label='Check!',choices=sentakushi)
    
    
    class Meta:
        model = ShippingOrder
        fields = [ 'fromshop', 'toshop', 'item', 'num']
    

class ShippingConfirmForm(forms.ModelForm):
    sentakushi = [
            [False,'未受取'],
            [True,'受取済']
            ]
    fromshop = forms.ModelChoiceField(label='出荷店',queryset=Shop.objects.all(), required=False)
    toshop = forms.ModelChoiceField(label='出荷先',queryset=Shop.objects.all(), required=False)
    item = forms.ModelChoiceField(label='商品名',queryset=Item.objects.all(), required=False)
    num = forms.IntegerField(label='数量')
    recieveFlag = forms.ChoiceField(label='checkbox',choices=sentakushi)
    
    
    class Meta:
        model = ShippingOrder
        fields = [ 'fromshop', 'toshop', 'item', 'num', 'recieveFlag']
    
