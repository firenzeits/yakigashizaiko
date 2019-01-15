# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 10:59:16 2018

@author: RYUICHI
"""

from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('update/<int:shopid>/', views.update, name='update'),
        path('shipping', views.shipping, name='shipping'),
        path('shippinghistory', views.shippinghistory, name='shippinghistory'),
        ]