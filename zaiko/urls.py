# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 10:59:16 2018

@author: RYUICHI
"""

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
        path('', views.index, name='index'),
        path('update/<int:shopid>/', views.update, name='update'),
        path('shipping', views.shipping, name='shipping'),
        path('shippinghistory', views.shippinghistory, name='shippinghistory'),
        path('shippingconfirm/<int:shippingid>/', views.shippingconfirm, name='shippingconfirm'),
        path('logout', auth_views.LogoutView.as_view(), name='logout'),
        
        ]