from django.core.management.base import BaseCommand, CommandError

from yekpay.models import Transaction


class Command(BaseCommand):
    help = 'Marks pending transactions older than 30 minutes ago as failed transaction'

    def handle(self, *args, **options):
        old_transactions = Transaction.objects.get_old_pending_transactions()
        print(f"found {old_transactions.count()} transactions.")
        old_transactions.update(status='FAILED')
        print("converted them to failed transactions.")
