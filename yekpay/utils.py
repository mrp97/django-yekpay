from random import randint

from .config import *
from .exceptions import *

def generate_yekpay_start_transaction_data(transaction_data):
    start_transaction_data = dict()
    start_transaction_data['toCurrencyCode'] = convert_currency_to_currency_code(transaction_data['toCurrencyCode'])
    start_transaction_data['fromCurrencyCode'] = convert_currency_to_currency_code(transaction_data['fromCurrencyCode'])
    start_transaction_data['merchantId'] = MERCHANTID
    start_transaction_data['orderNumber'] = transaction_data['order_number']
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

def get_call_back_url(transaction_data):
    if 'callback_url' in transaction_data:
        return transaction_data['callback_url']
    elif hasattr(settings,'YEKPAY_CALLBACK_URL'):
        return settings.YEKPAY_CALLBACK_URL
    else:
        raise CallbackUrlNotProvided("callback_url is not provided in the settings nor the transaction data")
