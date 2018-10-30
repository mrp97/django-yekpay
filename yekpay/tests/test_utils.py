#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-yekpay
------------

Tests for `django-yekpay` utils module.
"""
from yekpay import models,utils,config
from tests import sandbox_api

from django.test import TestCase
from django.http import  HttpRequest


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
        request = HttpRequest()
        request.method = 'Get'
        request.META['authority'] = 0
        response = utils.yekpay_process_transaction(
            request,
            sandbox_api.sandbox_yekpay_failed_transaction
        )
        self.assertFalse(response)


    def test_yekpay_process_transaction_return_true_for_success(self):
        """tests if process transaction returns true for code 100"""
        request = HttpRequest()
        request.method = 'Get'
        request.META['authority'] = 0
        response = utils.yekpay_process_transaction(
            request,
            sandbox_api.sandbox_yekpay_success_transaction
        )
        self.assertTrue(response)


    def tearDown(self):
        pass
