# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views


app_name = 'django_yekpay'
urlpatterns = [
    url(
        regex="^transactions/~create/$",
        view=views.transactionsCreateView.as_view(),
        name='transactions_create',
    ),
    url(
        regex="^transactions/~verify/$",
        view=views.verifyTransaction.as_view(),
        name='transactions_create',
    ),
    url(
        regex="^transactions/(?P<pk>\d+)/$",
        view=views.transactionsDetailView.as_view(),
        name='transactions_detail',
    ),
    # url(
    #     regex="^transactions/(?P<pk>\d+)/~update/$",
    #     view=views.transactionsUpdateView.as_view(),
    #     name='transactions_update',
    # ),
    url(
        regex="^transactions/$",
        view=views.transactionsListView.as_view(),
        name='transactions_list',
    ),
	]
