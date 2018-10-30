# -*- coding: utf-8 -*-

from django.db import models
from hashid_field import HashidField

from .config import CURRENCY_CHOICES, TRANSACTION_STATUS_CHIOCES
from .managers import TransactionManager

class Transaction(models.Model):
    amount = models.DecimalField(max_digits=64, decimal_places=2, default=0, blank=True, null=True)
    authorityStart = models.CharField(max_length=100,blank=True,null=True) #by module
    authorityVerify = models.CharField(max_length=100,blank=True,null=True) #by module
    description = models.TextField()
    callback_url = models.CharField(max_length=100)
    fromCurrencyCode = models.CharField(max_length=4, choices= CURRENCY_CHOICES, default='EUR')
    toCurrencyCode = models.CharField(max_length=4, choices= CURRENCY_CHOICES, default= 'EUR')
    firstName = models.CharField(max_length=225)
    lastName = models.CharField(max_length=225)
    email = models.CharField(max_length=225)
    mobile = models.CharField(max_length=225)
    orderNumber = HashidField(
        allow_int_lookup=True,
        blank=True,
        null=True
    )
    address = models.CharField(max_length=225)
    country = models.CharField(max_length=225)
    postalCode= models.CharField(max_length=225)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True) #by module
    status = models.CharField(max_length=100,choices= TRANSACTION_STATUS_CHIOCES) # by module
    failureReason = models.CharField(max_length=100,blank=True,null=True) # by module

    objects = TransactionManager()

    def __repr__(self):
        return '<yekpay id:{0}>'.format(self.orderNumber)

    def __str__(self):
        return "yekpay: {0}".format(self.orderNumber)
