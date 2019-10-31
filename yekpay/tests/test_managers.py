from django.test import TestCase

from .test_data import transaction_data
from ..models import Transaction


class TransactionManagerOrderNumberTestCase(TestCase):
    NUMBER_OF_TESTS_FOR_UNITY_CHECK = 10

    def test_generated_value_is_int(self):
        self.assertIsInstance(self.get_order_number(), int)

    def test_generated_values_are_unique(self):
        generated_values = set()
        for i in range(self.NUMBER_OF_TESTS_FOR_UNITY_CHECK):
            current_value = self.get_order_number()
            self.assertNotIn(current_value, generated_values)
            generated_values.add(current_value)

    def test_second_value_is_greater_than_the_first_one(self):
        first_value, second_value = self.get_order_number_value_pair()
        self.assertGreater(second_value, first_value)

    def get_order_number_value_pair(self):
        return (self.get_order_number(), self.get_order_number())

    def get_order_number(self):
        transaction = Transaction.objects.create_transaction(transaction_data)
        return transaction.order_number.id

