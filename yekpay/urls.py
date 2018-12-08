# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = 'yekpay'
urlpatterns = [
    # url(
    #     regex="^transactions/~create/$",
    #     view=views.yekpay_start_transaction(transaction_data),
    #     name='transactions_create',
    # ),
    # url(
    #     regex="^transactions/~verify/$",
    #     view=views.yekpay_proccess_transaction(),
    #     name='transactions_verify',
    # ),
    # url(
    #     regex="^transactions/(?P<pk>\d+)/$",
    #     view=views.transactionsDetailView.as_view(),
    #     name='transactions_detail',
    # ),
    # url(
    #     regex="^transactions/(?P<pk>\d+)/~update/$",
    #     view=views.transactionsUpdateView.as_view(),
    #     name='transactions_update',
    # ),
    # url(
    #     regex="^transactions/$",
    #     view=views.transactionsListView.as_view(),
    #     name='transactions_list',
    # ),
    path('sanbox-transaction/<int:authority_start>/',
         views.sandbox_pay,
         name='sandbox-payment'
    ),
    path('verify/<str:transaction_order_number>/',
        views.verify_transaction_view,
        name='verify_transaction'
    ),
	]
