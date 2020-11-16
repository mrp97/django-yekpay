import json, requests, uuid

from django.urls import reverse

from .config import *
from .models import Transaction
from .utils import generate_random_authority, convert_string_status_to_code


def request_yekpay_start(data):
    response_data = request_yekpay(gateway=YEKPAY_REQUEST_GATEWAY, data=data)
    return response_data


def request_yekpay_verify(data):
    response_data = request_yekpay(gateway=YEKPAY_VERIFY_GATEWAY, data=data)
    return response_data


def request_yekpay(gateway, data):
    json_data = json.dumps(data)
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(json_data)),
    }
    response = requests.post(gateway, headers=headers, data=json_data)
    return dict(json.loads(response.text))


def request_yekpay_start_simulation(data):
    yekpay_simulated_response = dict()
    yekpay_simulated_response["Code"] = 100
    yekpay_simulated_response["Authority"] = generate_random_authority()
    yekpay_simulated_response["Description"] = "Success"
    return yekpay_simulated_response


def request_yekpay_verify_simulation(data):
    yekpay_simulated_response = dict()
    transaction = Transaction.objects.filter(
        authority_verify=data["authority"]
    ).last()
    yekpay_simulated_response["OrderNo"] = transaction.order_number
    yekpay_simulated_response["Code"] = convert_string_status_to_code(
        transaction.status
    )
    return yekpay_simulated_response
