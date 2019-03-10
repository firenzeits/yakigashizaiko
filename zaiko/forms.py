# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 12:55:17 2018

@author: RYUICHI
"""

from django import forms
from .models import Item,Shop,ShippingOrder,StockStatus

    
class StockStatusForm(forms.ModelForm): 
    class Meta:
        model = StockStatus
        fields = ['item', 'num']
    
class ShippingOrderForm(forms.ModelForm):
    
    class Meta:
        model = ShippingOrder
        fields = [ 'fromshop', 'toshop', 'item', 'num']
    

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
    
