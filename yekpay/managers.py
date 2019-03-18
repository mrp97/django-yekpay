from datetime import timedelta

from django.db import models
from django.utils import timezone

from .config import YEKPAY_SIMULATION


class TransactionManager(models.Manager):
    """ Manager for :class:`Transaction` """

    def create_transaction(self, transaction_data):
        transaction_data['status'] = 'PENDING'
        transaction_data['simulation'] = YEKPAY_SIMULATION
        created_transaction = self.create(**transaction_data)
        created_transaction.order_number = created_transaction.id
        created_transaction.save(update_fields=['order_number'])
        return created_transaction

    def get_old_pending_transactions(self):
        return self.filter(
            created_at__lt=timezone.now() - timedelta(minutes=30),
            status='PENDING'
        )
