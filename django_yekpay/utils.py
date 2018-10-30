from .config import CURRENCY_CODES, TRANSACTION_STATUS_CODES

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
