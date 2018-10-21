# -*- coding: utf-8 -*-

from django.db import models

#from model_utils.models import TimeStampedModel


class Transaction(models.Model):
    amount = models.DecimalField(max_digits=64, decimal_places=2, default=0, blank=True, null=True)
    authority = models.IntegerField() #by module
    description = models.TextField()
    from_currency_code = models.IntegerField()
    to_currency_code = models.IntegerField()
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    email = models.CharField(max_length=225)
    mobile = models.CharField(max_length=225)
    orderNumber = models.CharField(max_length=500)
    address = models.CharField(max_length=225)
    country = models.CharField(max_length=225)
    postal_code= models.CharField(max_length=225)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True) #by module
    status = models.CharField(max_length=100) # by module

    def __repr__(self):
        return '<yekpay id:{0}>'.format(self.id)

    def __str__(self):
        return "yekpay: {0}".format(self.id)
