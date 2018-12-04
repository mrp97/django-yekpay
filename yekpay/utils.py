from random import randint

from django.apps import apps
from django.urls import reverse 
from django.utils import timezone

from .config import *
from .exceptions import *


def generate_yekpay_start_transaction_data(transaction):
    start_transaction_data = dict()
    start_transaction_data['merchantId'] = MERCHANTID
    start_transaction_data['amount'] = transaction.amount
    start_transaction_data['toCurrencyCode'] = convert_currency_to_currency_code(transaction.toCurrencyCoe)
    start_transaction_data['fromCurrencyCode'] = convert_currency_to_currency_code(transaction.fromCurrencyCode)
    start_transaction_data['orderNumber'] = transaction.orderNumber.hashid
    start_transaction_data['callback'] = get_call_back_url(transaction)
    start_transaction_data['firstName'] = transaction.first_name
    start_transaction_data['lastName'] = transaction.last_name
    start_transaction_data['email'] = transaction.email
    start_transaction_data['mobile'] = transaction.mobile
    start_transaction_data['address'] = transaction.address
    start_transaction_data['postalCode'] = transaction.postal_code
    start_transaction_data['country'] = transaction.country
    start_transaction_data['city'] = transaction.city
    start_transaction_data['description'] = transaction.description
    return start_transaction_data


def convert_currency_to_currency_code(currnecy):
    if currnecy in CURRENCY_CODES:
        return CURRENCY_CODES[currnecy]
    else:
        return None


def convert_status_code_to_string(statusCode):
    if statusCode in TRANSACTION_STATUS_CODES:
        return TRANSACTION_STATUS_CODES[statusCode]
    else:
        return None


def convert_string_status_to_code(status):
    INVERSE_TRANSACTION_STATUS_CODES = {status: code for code, status in TRANSACTION_STATUS_CODES.items()}
    if status in INVERSE_TRANSACTION_STATUS_CODES:
        return INVERSE_TRANSACTION_STATUS_CODES[status]
    else:
        return None


def generate_random_authority():
    return randint(10000,99999)


def get_call_back_url(transaction):
    if hasattr(settings,'YEKPAY_CALLBACK_URL'):
        return settings.YEKPAY_CALLBACK_URL
    else:
        return reverse(
            'yekpay:verify_transaction',
            kwargs = {
                'transaction_order_number': transaction.order_number.hashid
            }
        )


def get_transaction_from_trans_status(trans_status):
    if 'OrderNo' in trans_status:
        Transaction = apps.get_model('yekpay','Transaction')
        return Transaction.objects.filter(
            order_number=trans_status['OrderNo']
        ).last()
    return None


def process_transaction_trans_status(transaction,trans_status):
    if 'Code' in trans_status:
        status = convert_status_code_to_string(trans_status['Code'])
        if transaction:
            transaction.status = status
            if status == 'SUCCESS':
                transaction.successful_payment_date_time = timezone.now()
                transaction.save(update_fields=['status','successful_payment_date_time'])     
            elif status == 'FAILED':
                if 'PAYMENT_ERRORS' in trans_status:
                    transaction.failure_reason = trans_status['PAYMENT_ERRORS']
                else:
                    transaction.failure_reason = trans_status['Description']
                transaction.save(update_fields=['status','failure_reason'])           
            return transaction
    return None
