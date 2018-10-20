# -*- coding: utf-8 -*-

from django.db import models

#from model_utils.models import TimeStampedModel


class transactions(models.Model):
    amount = models.DecimalField(max_digits=64, decimal_places=2, default=0, blank=True, null=True)
    description = models.textField()
    from_currency_code = models.integerField()
    to_currency_code = models.integerField()
    first_name = models.charField(max_length=225)
    last_name = models.charField(max_length=225)
    email = models.charField(max_length=225)
    mobile = models.charField(max_length=225)
    address = models.charField(max_length=225)
    country = models.charField(max_length=225)
    postal_code= models.charField(max_length=225)
    city = models.charField(max_length=100)

    def __repr__(self):
        return '<yekpay id:{0}>'.format(self.id)

    def __str__(self):
        return "yekpay: {0}".format(self.id)