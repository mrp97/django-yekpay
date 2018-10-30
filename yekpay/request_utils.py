import json, requests, uuid

from django.urls import reverse

from .config import YEKPAY_START_GATEWAY, YEKPAY_REQUEST_GATEWAY, YEKPAY_VERIFY_GATEWAY
from .models import Transaction
from .utils import generate_random_authority, convert_string_status_to_code

def request_yekpay_start(data):
    response_data = request_yekpay(
        gateway= YEKPAY_REQUEST_GATEWAY,
        data= data
    )
    response_data.update({
        'YekpayStartUrl': YEKPAY_START_GATEWAY + str(response_data['Authority'])
    })
    return response_data

def request_yekpay_verify(data):
    response_data = request_yekpay(
        gateway= YEKPAY_VERIFY_GATEWAY,
        data= data
    )
    return response_data

def request_yekpay(gateway,data):
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json', 'Content-Length': str(len(json_data))}
    response = requests.post(gateway, headers=headers, data=json_data)
    return dict(json.loads(response.text))

def request_yekpay_start_simulation(data):
    yekpaySimulatedResponse = dict()
    yekpaySimulatedResponse['Code'] = 100
    yekpaySimulatedResponse['Authority'] = generate_random_authority()
    yekpaySimulatedResponse['Description'] = "Success"
    yekpaySimulatedResponse['YekpayStartUrl'] = reverse(
        'yekpay:sandbox-payment',
        kwargs={
            'authority_start': yekpaySimulatedResponse['Authority']
        }
    )
    return yekpaySimulatedResponse

def request_yekpay_verify_simulation(data):
    yekpaySimulatedResponse = dict()
    transaction = Transaction.objects.filter(authorityVerify= data['authority']).last()
    yekpaySimulatedResponse['OrderNo']= transaction.orderNumber
    yekpaySimulatedResponse['Code']= convert_string_status_to_code(transaction.status)
    return yekpaySimulatedResponse
