import uuid

def sandbox_yekpay_start(gateway, data):
    response = uuid.uuid4()
    return response


def sandbox_yekpay_failed_transaction(gateway, data):
    verify_transaction_data = {
        'Code': -10,
        'Description': 'payment is incomplete with error',
    }
    return verify_transaction_data


def sandbox_yekpay_success_transaction(gateway, data):
    verify_transaction_data = {
        'Code': 100,
        'Description': 'paymenet was successful'
    }
    return verify_transaction_data

