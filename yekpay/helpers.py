# -*- coding: utf-8 -*-
import  logging
from time import time
from django.conf import settings

from .models import (
    Transaction,
)
from .config import *
from .exceptions import *
from .request_utils import ( request_yekpay, request_yekpay_start,
    request_yekpay_verify, request_yekpay_start_simulation,
    request_yekpay_verify_simulation )
from .utils import ( convert_status_code_to_string,
    convert_currency_to_currency_code, get_call_back_url,
    generate_yekpay_start_transaction_data, process_transaction_trans_status )

logging.basicConfig(level=logging.DEBUG)

def yekpay_start_transaction(transaction_data,request_function=request_yekpay_start):
    if YEKPAY_SIMULATION:
        request_function = request_yekpay_start_simulation
    transaction = Transaction.objects.create_transaction(transaction_data)
    start_transaction_data = generate_yekpay_start_transaction_data(transaction)
    logging.info('starting transaction',transaction.order_number)
    yekpay_response_data = request_function(
        data= start_transaction_data
    )
    if yekpay_response_data['Code'] == 100:
        logging.info("returning redirecting url to yekpay's gateway")
        transaction.authorityStart = str(yekpay_response_data['Authority'])
        transaction.save(update_fields=['authorityStart'])
        return transaction
    else:
        logging.error('django_yekpay error' + str(yekpay_response_data['Description']) + str(yekpay_response_data['Code']))
        return None

def yekpay_process_transaction(request, request_function=request_yekpay_verify):
    if YEKPAY_SIMULATION:
        request_function = request_yekpay_verify_simulation
    trans_status = request_function(
        data=  {
            "merchantId": MERCHANTID,
            "authority": request.GET['authority']
        }
    )
    transaction = get_transaction_from_trans_status(
        trans_status
    )
    if transaction:
        transaction.authority_verfiy = request.GET['authority']
        trasaction.save(update_fields='authority_verify')
    transaction = process_transaction_trans_status(
        transaction,
        trans_status
    )
    return transaction