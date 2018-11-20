
class YekpayException(Exception):
    """ yekpay general exception """

class UnknownTransactionFailure(YekpayException):
    """ Unknown transaction failure """

class UnknownTransactionStatusCode(YekpayException):
    """ Unknown transaction status code """

class CallbackUrlNotProvided(YekpayException):
    """ callback url is not provided in transaction data or project settings """