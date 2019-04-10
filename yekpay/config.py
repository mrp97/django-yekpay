from django.conf import settings

MERCHANTID = getattr(settings, "YEKPAY_MERCHANT_ID", "")
YEKPAY_SIMULATION = getattr(settings, "YEKPAY_SIMULATION", False)
YEKPAY_CALLBACK_URL = getattr(settings, 'YEKPAY_CALLBACK_URL', None)
YEKPAY_START_GATEWAY = "https://gate.yekpay.com/api/payment/start/"
YEKPAY_VERIFY_GATEWAY = "https://gate.yekpay.com/api/payment/verify"
YEKPAY_REQUEST_GATEWAY = "https://gate.yekpay.com/api/payment/request"
CURRENCY_CODES = {
    "EUR": 978,  # Euro
    "IRR": 364,  # Iranian Rial
    "CHF": 756,  # Swiss Franc
    "AED": 784,  # United Arab Emirates Dirham
    "CNY": 156,  # Chinese Yuan
    "GBP": 826,  # British Pound
    "JPY": 392,  # Japanese 100 Yens
    "RUB": 643,  # Russian Ruble
    "TRY": 949,  # Turkish New Lira
}

CURRENCY_CHOICES = (
    ("EUR", "Euro"),
    ("IRR", "Iranian Rial"),
    ("CHF", "Swiss Franc"),
    ("AED", "United Arab Emirates Dirham"),
    ("CNY", "Chinese Yuan"),
    ("GBP", "British Pound"),
    ("JPY", "Japanese 100 Yens"),
    ("RUB", "Russian Ruble"),
    ("TRY", "Turkish New Lira"),
)
TRANSACTION_STATUS_CODES = {
    -1: "INCOMPLETE_PARAMETERS",
    -2: "MERCHANT_CODE_INCORRECT",
    -3: "MERCHANT_CODE_NOT_ACTIVE",
    -8: "AUTHORITY_CODE_INVALID",
    -9: "ALREADY_VERIFIED",
    -10: "FAILED",
    -100: "UNKNOWN",
    100: "SUCCESS",
}

INVERSE_TRANSACTION_STATUS_CODES = {
    status: code for code, status in TRANSACTION_STATUS_CODES.items()
}

TRANSACTION_STATUS_CHOICES = (
    ("PENDING", "Transaction has just started"),
    ("INCOMPLETE_PARAMETERS", "Transaction parameters were incomplete"),
    ("MERCHANT_CODE_INCORRECT", "Merchant code was incorrect"),
    ("MERCHANT_CODE_NOT_ACTIVE", "Merchant code is not active"),
    ("AUTHORITY_CODE_INVALID", "Authority code was invalid"),
    ("ALREADY_VERIFIED", "Transaction was already verified"),
    ("FAILED", "Transaction was failed"),
    ("UNKNOWN", "Transaction was failed with unknown error"),
    ("SUCCESS", "Transaction was successfully done"),
)

FAILURE_REASONS = ["test transaction failed"]
