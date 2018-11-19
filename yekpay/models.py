# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from hashid_field import HashidField

from .config import CURRENCY_CHOICES, TRANSACTION_STATUS_CHIOCES, YEKPAY_START_GATEWAY
from .managers import TransactionManager

class Transaction(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
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
    simulation = models.BooleanField(default=False)
    objects = TransactionManager()

    def __repr__(self):
        return '<yekpay id:{0}>'.format(self.orderNumber)

    def __str__(self):
        return "yekpay: {0}".format(self.orderNumber)

    def get_transaction_start_url(self):
        if self.simulation is True:
            return YEKPAY_START_GATEWAY + self.authorityStart
        else:
            return reverse(
                'yekpay:sandbox-payment',
                kwargs={
                    'authority_start': self.authorityStart
                }
            )
