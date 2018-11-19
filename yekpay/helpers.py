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
    generate_yekpay_start_transaction_data )

logging.basicConfig(level=logging.DEBUG)

def yekpay_start_transaction(transaction_data,request_function=request_yekpay_start):
    if YEKPAY_SIMULATION:
        request_function = request_yekpay_start_simulation
    transaction_data['callback_url']= get_call_back_url(transaction_data)
    transaction = Transaction.objects.create_transaction(transaction_data)
    transaction_data['order_number'] = transaction.orderNumber.id
    start_transaction_data = generate_yekpay_start_transaction_data(transaction_data)
    print(start_transaction_data)
    logging.info('starting transaction',transaction_data['order_number'])
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
    if 'Code' in trans_status:
        status = convert_status_code_to_string(trans_status['Code'])
        if status == 'SUCCESS':
            transaction = Transaction.objects.get(orderNumber=trans_status['OrderNo'])
            transaction.authorityVerify = str(request.GET['authority'])
            transaction.status = 'SUCCESS'
            transaction.save(update_fields=['status', 'authorityVerify'])
            logging.info(f'Transaction {transaction.orderNumber.id} was successfull')
            return transaction
        elif status == 'FAILED':
            if 'OrderNo' in trans_status:
                transaction = Transaction.objects.get(orderNumber=trans_status['OrderNo'])
                transaction.authorityVerify = str(request.GET['authority'])
                transaction.status = 'FAILED'
                if 'PAYMENT_ERRORS' in trans_status:
                    transaction.failureReason = trans_status['PAYMENT_ERRORS']
                else:
                    transaction.failureReason = trans_status['Description']
                transaction.save(update_fields=['status','authorityVerify','failureReason'])
                logging.info(trans_status)
                return transaction
            else:
                logging.error(f'Transaction failed {trans_status}')
                return None
    else:
        return None

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
