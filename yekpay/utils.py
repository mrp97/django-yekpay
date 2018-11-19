from random import randint

from .config import *
from .exceptions import *

def generate_yekpay_start_transaction_data(transaction_data):
    start_transaction_data = dict()
    start_transaction_data['merchantId'] = MERCHANTID
    start_transaction_data['amount'] = transaction_data['amount']
    start_transaction_data['toCurrencyCode'] = convert_currency_to_currency_code(transaction_data['to_currency_code'])
    start_transaction_data['fromCurrencyCode'] = convert_currency_to_currency_code(transaction_data['from_currency_code'])
    start_transaction_data['orderNumber'] = transaction_data['order_number']
    start_transaction_data['callback'] = transaction_data['callback_url']
    start_transaction_data['firstName'] = transaction_data['first_name']
    start_transaction_data['lastName'] = transaction_data['last_name']
    start_transaction_data['email'] = transaction_data['email']
    start_transaction_data['mobile'] = transaction_data['mobile']
    start_transaction_data['address'] = transaction_data['address']
    start_transaction_data['postalCode'] = transaction_data['postal_code']
    start_transaction_data['country'] = transaction_data['country']
    start_transaction_data['city'] = transaction_data['city']
    start_transaction_data['description'] = transaction_data['description']
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
