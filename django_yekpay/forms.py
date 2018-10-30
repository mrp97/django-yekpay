# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from .models import Transaction

class YekpayTransactionForm(forms.Form):
    class Meta:
        model = Transaction
        exclude = ['created_at']
