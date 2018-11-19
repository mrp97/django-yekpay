from django.conf import settings
from django.db import models

from .exceptions import *
from .config import YEKPAY_SIMULATION
class TransactionManager(models.Manager):
    """ Manager for :class:`Transaction` """

    def create_transaction(self, transaction_data):
        transaction_data['status'] = 'PENDING'
        transaction_data['simulation'] = YEKPAY_SIMULATION
        createdTransaction = self.create(**transaction_data)
        createdTransaction.orderNumber = createdTransaction.id
        createdTransaction.save(update_fields=['orderNumber'])
        return createdTransaction
