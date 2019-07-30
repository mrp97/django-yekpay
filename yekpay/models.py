# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from hashid_field import HashidField
from urllib import parse as urlparse
from urllib.parse import urlencode
from .config import CURRENCY_CHOICES, TRANSACTION_STATUS_CHOICES, YEKPAY_START_GATEWAY
from .exceptions import *
from .managers import TransactionManager


class Transaction(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(
        max_digits=64, decimal_places=2, default=0, blank=True, null=True
    )
    authority_start = models.CharField(
        max_length=100, blank=True, null=True
    )  # by module
    authority_verify = models.CharField(
        max_length=100, blank=True, null=True
    )  # by module
    description = models.TextField()
    callback_url = models.CharField(max_length=100)
    from_currency_code = models.CharField(
        max_length=4, choices=CURRENCY_CHOICES, default="EUR"
    )
    to_currency_code = models.CharField(
        max_length=4, choices=CURRENCY_CHOICES, default="EUR"
    )
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    email = models.CharField(max_length=225)
    mobile = models.CharField(max_length=225)
    order_number = HashidField(allow_int_lookup=True, blank=True, null=True)
    address = models.CharField(max_length=225)
    country = models.CharField(max_length=225)
    postal_code = models.CharField(max_length=225)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)  # by module
    successful_payment_date_time = models.DateTimeField(
        blank=True, null=True
    )  # by module
    status = models.CharField(
        max_length=100, choices=TRANSACTION_STATUS_CHOICES
    )  # by module
    failure_reason = models.CharField(
        max_length=100, blank=True, null=True
    )  # by module
    simulation = models.BooleanField(default=False)
    objects = TransactionManager()

    class Meta:
        ordering = ['-created_at']

    def __repr__(self):
        return "<yekpay id:{0}>".format(self.order_number)

    def __str__(self):
        return "yekpay: {0}".format(self.order_number)
    
    def get_order_number(self):
        return self.order_number.hashid

    def success(self):
        self.status = "SUCCESS"
        self.successful_payment_date_time = timezone.now()
        self.save(update_fields=["status", "successful_payment_date_time"])

    def fail(self, failure_reason=None):
        self.status = "FAILED"
        if failure_reason:
            self.failure_reason = failure_reason
        self.save(update_fields=["status", "failure_reason"])

    def is_successful(self):
        return self.status == "SUCCESS"

    def get_transaction_start_url(self, request=None):
        if self.simulation is False:
            return YEKPAY_START_GATEWAY + self.authority_start
        else:
            relative_start_url = reverse(
                "yekpay:sandbox-payment",
                kwargs={"authority_start": self.authority_start},
            )
            if request:
                return request.build_absolute_uri(relative_start_url)
            else:
                return relative_start_url

    def get_verify_url(self):
        return (
            reverse(
                "yekpay:verify_transaction",
                kwargs={"transaction_order_number": self.order_number.hashid},
            )
            + f"?authority={self.authority_verify}"
        )

    def get_client_callback_url(self):
        if self.callback_url:
            url_parts = list(urlparse.urlparse(self.callback_url))
            query = dict(urlparse.parse_qsl(url_parts[4]))
            params = {'orderNumber': self.order_number}
            query.update(params)
            url_parts[4] = urlencode(query)
            print(urlparse.urlunparse(url_parts))
            return urlparse.urlunparse(url_parts)
        else:
            raise CallbackUrlNotProvided(
                f"Callback url is not set in transaction with order number {self.order_number.hashid}"
            )
