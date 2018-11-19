#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-yekpay
------------

Tests for `django-yekpay` utils module.
"""

from django.test import TestCase
from django.http import  HttpRequest

from yekpay import models,utils,config
from .sandbox_api import *
from .test_data import transaction_data
class TestDjango_yekpay_utils(TestCase):

    def setUp(self):
        transaction = models.Transaction.objects.create_transaction(transaction_data)
        transaction.orderNumber = 1
        transaction.save(update_fields=['orderNumber'])


    def test_yekpay_start_transaction_returns_gateway(self):
        """tests if user get redirected to yekpay's gateway"""
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
            .sandbox_yekpay_failed_transaction
        )
        self.assertFalse(response)


    def test_yekpay_process_transaction_return_true_for_success(self):
        """tests if process transaction returns true for code 100"""
        request = HttpRequest()
        request.method = 'Get'
        request.META['authority'] = 0
        response = utils.yekpay_process_transaction(
            request,
            .sandbox_yekpay_success_transaction
        )
        self.assertTrue(response)


    def tearDown(self):
        pass
