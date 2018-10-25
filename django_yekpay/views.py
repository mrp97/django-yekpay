# -*- coding: utf-8 -*-
import requests, json, logging, uuid
from time import time

from django.shortcuts import render, HttpResponse
from .models import Transaction
from django.views.generic import (
    UpdateView,
    DetailView,
    ListView
)

from .utils import yekpay_process_transaction

def sandbox_pay(request, authoritys):
    return render(request,
                  'django_yekpay/sand-box.html',
                  {'authoritys': authoritys, 'authorityv': uuid.uuid4()}
                  )

def success(request):
    transaction = Transaction.objects.get(authorityStart=str(request.GET['authoritys']))
    transaction.authorityVerify = str(request.GET['authority'])
    transaction.status = 'SUCCESS'
    transaction.save(update_fields=['authorityVerify','Status'])
    return HttpResponse(yekpay_process_transaction(request))

def fail(request):
    transaction = Transaction.objects.get(authorityStart=str(request.GET['authoritys']))
    transaction.authorityVerify = str(request.GET['authority'])
    transaction.status = 'FAILED'
    transaction.save(update_fields=['authorityVerify', 'Status'])
    yekpay_process_transaction(request)

# class transactionsDetailView(DetailView):
#     model = transactions
#
#
# class transactionsListView(ListView):
#     model = transactions
