from django.db import models


class TransactionManager(models.Manager):
    """ Manager for :class:`Transaction` """

    def create_transaction(self, transactionData):
        createdTransaction = self.create(**transactionData)
        createdTransaction.status = 'PENDING'
        createdTransaction.orderNumber = createdTransaction.id
        createdTransaction.save()
        return createdTransaction
