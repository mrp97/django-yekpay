# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import include
from django.urls import re_path


urlpatterns = [
    re_path(r'^', include('yekpay.urls', namespace='yekpay')),
]
