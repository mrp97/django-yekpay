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
    request_yekpay_simulation )
from .utils import convert_status_code_to_string, convert_currency_to_currency_code

# constants
MERCHANTID = getattr(settings, 'YEKPAY_MERCHANT_ID', '')
YEKPAY_SIMULATION = getattr(settings, 'YEKPAY_SIMULATION', False)
logging.basicConfig(level=logging.DEBUG)

def yekpay_start_transaction(transaction_data,request_function=request_yekpay_start):
    if YEKPAY_SIMULATION:
        request_function = request_yekpay_simulation
    global MERCHANTID
    transaction = Transaction.objects.create_transaction(transaction_data)
    transaction_data['toCurrencyCode'] = convert_currency_to_currency_code(transaction_data['toCurrencyCode'])
    transaction_data['fromCurrencyCode'] = convert_currency_to_currency_code(transaction_data['fromCurrencyCode'])
    if 'callback' in transaction_data:
        config = {
            "merchantId": MERCHANTID,
            'orderNumber': transaction.orderNumber.id
        }
    else:
        config = {
            "merchantId": MERCHANTID,
            "callback": getattr(settings, 'YEKPAY_CALLBACK_URL', ''),
            'orderNumber': transaction.orderNumber.id
        }
    transaction.redirect_url = config['callback']
    transaction.save(update_fields=['redirect_url'])
    logging.info('start transaction',config['orderNumber'])
    start_transaction_data = {**config, **transaction_data}
    yekpay_response_data = request_function(
        data= start_transaction_data
    )
    if yekpay_response_data['Code'] == 100:
        logging.info("returning redirecting url to yekpay's gateway")
        transaction.authorityStart = str(yekpay_response_data['Authority'])
        transaction.save()
        return yekpay_response_data['YekpayStartUrl']
    else:
        logging.error('django_yekpay error' + str(yekpay_response_data['Description']) + str(yekpay_response_data['Code']))
        return None

def yekpay_process_transaction(request, request_function=request_yekpay):

    global MERCHANTID
    verify_transaction_data = {
        "merchantId": MERCHANTID,
        "authority": request.GET['authority']
    }
    trans_status = request_function(
        gateway=YEKPAY_VERIFY_GATEWAY,
        data= verify_transaction_data
    )
    if 'Code' in trans_status:
        status = convert_status_code_to_string(trans_status['Code'])
        if status == 'SUCCESS':
            transaction = Transaction.objects.get(orderNumber=trans_status['OrderNo'])
            transaction.authorityVerify = str(request.GET['authority'])
            transaction.save(update_fields=['status', 'authorityVerify'])
        elif status == 'FAILED':
            if 'OrderNo' in trans_status:
                transaction = Transaction.objects.get(orderNumber=trans_status['OrderNo'])
                transaction.authorityVerify = str(request.GET['authority'])
                if 'PAYMENT_ERRORS' in trans_status:
                    transaction.failureReason = trans_status['PAYMENT_ERRORS']
                else:
                    transaction.failureReason = trans_status['Description']
                transaction.save(update_fields=['status','authorityVerify','failureReason'])
                logging.info(trans_status)
                return False
            else:
                return False

    # else:
    #     transaction = Transaction.objects.get(authorityVerify=request.GET['authority'])
    #     if transaction.status == 'SUCCESS':
    #         return True
    #     else:
    #         return transaction.status

        # if 'Code' in trans_status:
        #     logging.info('verfiy',trans_status['OrderNo'])
        #     transaction = Transaction.objects.get(orderNumber=trans_status['OrderNo'])
        #     transaction.authorityVerify =  str(request.GET['authority'])
        #     status = convert_status_code_to_string(trans_status['Code'])
        #     if status:
        #         transaction.status = status
        #         if status == 'SUCCESS':
        #             # transaction_succeed
        #             transaction.save(update_fields=['status','authorityVerify'])
        #             return True
        #         elif status == 'FAILED':
        #             # transaction_failed
        #             transaction.failureReason = trans_status['PAYMENT_ERRORS']
        #             transaction.save(update_fields=['status','authorityVerify','failureReason'])
        #             logging.info(trans_status)
        #             return False
        #         else:
        #             transaction.save(update_fields=['status','authorityVerify'])
        #             logging.info(trans_status)
        #             return False
        #     else:
        #         raise UnknownTransactionStatusCode("Status code was not found in defined status codes in yekpay.config!")
        #
        # else:
        #     logging.error(trans_status)
        #     raise UnknownTransactionFailure('There was an unknown problem in payment!')
