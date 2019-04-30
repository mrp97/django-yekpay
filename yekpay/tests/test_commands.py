from datetime import timedelta
from io import StringIO

from django.core.management import call_command
from django.utils import timezone

from ShipUp.test import TestCase
from mock import patch, Mock

from yekpay.models import Transaction
from yekpay.tests.test_data import transaction_data


class CommandsTestCase(TestCase):
    def setUp(self):
        Transaction.objects.create(
            **transaction_data
        )
        # create object that is for 30 minutes ago
        thirty_minutes_ago = timezone.now() - timedelta(minutes=31)
        with patch('django.utils.timezone.now', Mock(return_value=thirty_minutes_ago)):
            Transaction.objects.create(
                **transaction_data
            )

    def test_export_container_numbers_without_arguments(self):
        """
        Test remove pending transactions
        :return:
        """
        output = StringIO()
        call_command('remove_pending_transactions', stdout=output)
        self.assertMatchSnapshot(
            output.getvalue()
        )
