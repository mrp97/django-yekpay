# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = 'yekpay'
urlpatterns = [
    path('sanbox-transaction/<int:authority_start>/',
         views.sandbox_pay,
         name='sandbox-payment'
    ),
    path('verify/<str:transaction_order_number>/',
        views.verify_transaction_view,
        name='verify_transaction'
    ),
	]
