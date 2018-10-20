# -*- coding: utf-8 -*-
import requests, json

from django.views.generic import (
    UpdateView,
    DetailView,
    ListView
)

from django.shortcuts import HttpResponseRedirect
from django.urls import reverse

from .models import (
    Transaction,
)
from .config import *

# constants
MERCHANTID = getattr('settings', 'YEKPAY_MERCHANT_ID')


def yekpay_start_transaction(request, transaction_data):
    global MERCHANTID

    config = {
        "merchantId": MERCHANTID,
        "callback": getattr('settings', 'YEKPAY_CALLBACK_URL')
    }
    data = {**config, **transaction_data}
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json', 'Content-Length': str(len(json_data))}
    response = requests.post(YEKPAY_REQUEST_GATEWAY, headers=headers, data=json_data)
    authority = dict(json.loads(response.text))
    if authority['Code'] == 100:
        HttpResponseRedirect(YEKPAY_START_GATEWAY + str(authority['Authority']))
    else:
        print(authority['Description'] + authority['Code'])


def yekpay_proccess_transaction(request):
    global MERCHANTID
    verify_transaction_data = {
        "merchantId": MERCHANTID,
        "authority": request.GET['authority']
    }
    json_data = json.dumps(verify_transaction_data)
    headers = {'Content-Type': 'application/json', 'Content-Length': str(len(json_data))}
    response = requests.post(YEKPAY_VERIFY_GATEWAY, headers=headers, data=json_data)
    trans_status = dict(json.loads(response.text))
    if trans_status['Code'] == 100:
        return True
        # transaction_succeed
    else:
        return False
        # transaction_failed


class transactionsDetailView(DetailView):
    model = transactions


class transactionsListView(ListView):
    model = transactions
