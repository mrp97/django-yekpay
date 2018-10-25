#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-yekpay
------------

Tests for `django-yekpay` models module.
"""

from django.test import TestCase

from django_yekpay import models,utils


class TestDjango_yekpay(TestCase):

    def setUp(self):
        pass

    def test_something(self):
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
        utils.yekpay_start_transaction(transaction_data,request_function=utils.sandbox_yekpay)

    def tearDown(self):
        pass
