from datetime import timedelta
from django.db import models
from django.utils import timezone
import time

from .config import YEKPAY_SIMULATION


class TransactionManager(models.Manager):
    """ Manager for :class:`Transaction` """

    def create_transaction(self, transaction_data):
        transaction_data["status"] = "PENDING"
        transaction_data["simulation"] = YEKPAY_SIMULATION
        created_transaction = self.create(**transaction_data)
        created_transaction.order_number = self.generate_uniq_order_number()
        created_transaction.save(update_fields=["order_number"])
        return created_transaction

    def generate_uniq_order_number(self):
        order_number = self._generate_order_number()
        while self.filter(order_number=order_number).exists():
            order_number += 1
        return order_number

    def _generate_order_number(self):
        return int(round(time.time()))

    def get_old_pending_transactions(self):
        return self.filter(
            created_at__lt=timezone.now() - timedelta(minutes=30),
            status="PENDING",
        )
