import json, requests, uuid

from django.urls import reverse

from .config import YEKPAY_START_GATEWAY, YEKPAY_REQUEST_GATEWAY

def request_yekpay_start(data):
    response_data = request_yekpay(
        gateway= YEKPAY_REQUEST_GATEWAY,
        data= data
    )
    response_data.update({
        'YekpayStartUrl': YEKPAY_START_GATEWAY + str(response_data['Authority'])
    })
    return response_data

def request_yekpay(gateway,data):
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json', 'Content-Length': str(len(json_data))}
    response = requests.post(gateway, headers=headers, data=json_data)
    return dict(json.loads(response.text))

def request_yekpay_simulation(data):
    yekpaySimulatedResponse = dict()
    yekpaySimulatedResponse['Code'] = 100
    yekpaySimulatedResponse['Authority'] = uuid.uuid4()
    yekpaySimulatedResponse['Description'] = "Success"
    yekpaySimulatedResponse.update({
        'YekpayStartUrl': reverse(
            'yekpay:sandbox-payment',
            kwargs={
                'authoritys': yekpaySimulatedResponse['Authority']
            }
        )
    })
    return yekpaySimulatedResponse
