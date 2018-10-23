# -*- coding: utf-8 -*-
import requests, json, logging
from time import time
from django.shortcuts import HttpResponseRedirect
from django.conf import settings

from .models import (
    Transaction,
)
from .config import *
from .exceptions import *

# constants
MERCHANTID = getattr(settings, 'YEKPAY_MERCHANT_ID', '')

def yekpay_start_transaction(transaction_data):
    global MERCHANTID

    transaction = Transaction.objects.create_transaction(transaction_data)
    config = {
        "merchantId": MERCHANTID,
        "callback": getattr(settings, 'YEKPAY_CALLBACK_URL', ''),
        'orderNumber': transaction.orderNumber
    }
    start_transaction_data = {**config, **transaction_data}
    authority = request_yekpay(
        gateway=YEKPAY_REQUEST_GATEWAY,
        data= start_transaction_data
    )
    if authority['Code'] == 100:
        logging.info("returning redirecting url to yekpay's gateway")
        return (YEKPAY_START_GATEWAY + str(authority['Authority']))
    else:
        logging.info('django_yekpay error' + str(authority['Description']) + str(authority['Code']))
        return None

def yekpay_proccess_transaction(request):
    global MERCHANTID
    verify_transaction_data = {
        "merchantId": MERCHANTID,
        "authority": request.GET['authority']
    }

    trans_status = request_yekpay(
        gateway=YEKPAY_VERIFY_GATEWAY,
        data= verify_transaction_data
    )
    if 'Code' in trans_status:
        transaction = Transaction.objects.get(orderNumber=trans_status['OrderNo'])
        status = convert_status_code_to_string(trans_status['Code'])
        if status:
            transaction.status = status
            if status == 'SUCCESS':
                # transaction_succeed
                transaction.save(update_fields=['status'])
                return True
            elif status == 'FAILED':
                # transaction_failed
                transaction.failureReason = trans_status['PAYMENT_ERRORS']
                transaction.save(update_fields=['status','failureReason'])
                logging.info(trans_status)
                return False
            else:
                transaction.save(update_fields=['status'])
                logging.info(trans_status)
                return False
        else:
            raise UnknownTransactionStatusCode("Status code was not found in defined status codes in yekpay.config!")

    else:
        logging.error(trans_status)
        raise UnknownTransactionFailure('There was an unknown problem in payment!')

def request_yekpay(gateway,data):
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json', 'Content-Length': str(len(json_data))}
    response = requests.post(gateway, headers=headers, data=json_data)
    return dict(json.loads(response.text))

def convert_status_code_to_string(statusCode):
    if statusCode in TRANSACTION_STATUS_CODES:
        return TRANSACTION_STATUS_CODES[statusCode]
    else:
        return None
