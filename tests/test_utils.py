#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-yekpay
------------

Tests for `django-yekpay` utils module.
"""

from django.test import TestCase

from django_yekpay import models,utils,config


class TestDjango_yekpay_utils(TestCase):

    def setUp(self):
        transaction_data = {
            "amount": 10000,
            "description": "some plan",
            "fromCurrencyCode": 'IRR',
            "toCurrencyCode": 'IRR',
            "firstName": 'ship',
            "lastName": "up",
            "email": "ex@example.com",
            "mobile": "+4455884976",
            "address": "tehran",
            "country": "Unaited Arab Emirates",
            "postalCode": "64976",
            "city": "Dubai",
        }
        transaction = models.Transaction.objects.create_transaction(transaction_data)
        transaction.orderNumber = 1
        transaction.save(update_fields=['orderNumber'])

    def test_yekpay_start_transaction_returns_gateway(self):
        """tests if user get redirected to yekpay's gateway"""
        transaction_data = {
            "amount": 10000,
            "description": "some plan",
            "fromCurrencyCode": 'IRR',
            "toCurrencyCode": 'IRR',
            "firstName": 'ship',
            "lastName": "up",
            "email": "ex@example.com",
            "mobile": "+4455884976",
            "address": "tehran",
            "country": "Unaited Arab Emirates",
            "postalCode": "64976",
            "city": "Dubai",
        }
        response = utils.yekpay_start_transaction(transaction_data)
        self.assertIn('Code', response[1])
        self.assertIn('Authority', response[1])
        self.assertIn('Description', response[1])

    def test_yekpay_process_transaction_retrun_false_for_failed(self):
        """tests if process transaction """
        verify_transaction_data = {
            'Code': -10,
            'Description': 'payment is incomplete with error',
        }
        response = utils.yekpay_process_transaction(None,verify_transaction_data)
        self.assertFalse(response)

    def test_yekpay_process_transaction_return_ture_for_success(self):
        """tests if process transaction returns true for code 100"""
        verify_transaction_data = {
            'Code': 100,
            'Description': 'paymenet was successful'
        }
        response = utils.yekpay_process_transaction(
            None,verify_transaction_data
        )
        self.assertTrue(response)

    def tearDown(self):
        pass
