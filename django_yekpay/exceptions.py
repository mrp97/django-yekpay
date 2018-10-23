
class YekpayException(Exception):
    """ yekpay general exception """

class UnknownTransactionFailure(YekpayException):
    """ Unknown transaction failure """

class UnknownTransactionStatusCode(YekpayException):
    """ Unknown transaction status code """
