#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-yekpay
------------

Tests for `django-yekpay` utils module.
"""
from unittest import skip
from django.test import TestCase
from django.http import  HttpRequest

from yekpay import models,utils,config
from .sandbox_api import *
from .test_data import transaction_data

class TestDjango_yekpay_utils(TestCase):

    def setUp(self):
        self.transaction = models.Transaction.objects.create_transaction(transaction_data)
        self.successful_trans_status = {
            'Code': 100,
            'OrderNo': self.transaction.order_number.id
        }
        self.failed_trans_status = {
            'Code': -10,
        }

    @skip('')
    def test_yekpay_start_transaction_returns_gateway(self):
        """tests if user get redirected to yekpay's gateway"""
        response = utils.yekpay_start_transaction(transaction_data)
        self.assertIn('Code', response[1])
        self.assertIn('Authority', response[1])
        self.assertIn('Description', response[1])

    @skip('')
    def test_yekpay_process_transaction_retrun_false_for_failed(self):
        """tests if process transaction """
        request = HttpRequest()
        request.method = 'Get'
        request.META['authority'] = 0
        response = utils.yekpay_process_transaction(
            request,
            sandbox_yekpay_failed_transaction
        )
        self.assertFalse(response)

    @skip('')
    def test_yekpay_process_transaction_return_true_for_success(self):
        """tests if process transaction returns true for code 100"""
        request = HttpRequest()
        request.method = 'Get'
        request.META['authority'] = 0
        response = utils.yekpay_process_transaction(
            request,
            sandbox_yekpay_success_transaction
        )
        self.assertTrue(response)
    
    
    def test_get_transaction_from_trans_status(self):
        self.assertEqual(
            self.transaction,
            utils.get_transaction_from_trans_status(
                self.successful_trans_status
            )
        )
        self.assertIsNone(
            utils.get_transaction_from_trans_status(
                self.failed_trans_status
            )
        )

    def tearDown(self):
        pass
