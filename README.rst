=============================
Django yekpay
=============================

.. image:: https://badge.fury.io/py/django-yekpay.svg
    :target: https://badge.fury.io/py/django-yekpay

.. image:: https://travis-ci.org/Glyphack/django-yekpay.svg?branch=master
    :target: https://travis-ci.org/Glyphack/django-yekpay

.. image:: https://codecov.io/gh/Glyphack/django-yekpay/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Glyphack/django-yekpay

multicurrency transactions in django using yekpay service

Documentation
-------------

The full documentation is at https://django-yekpay.readthedocs.io.

Quickstart
----------

Install Django yekpay::

    pip install django-yekpay

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_yekpay.apps.DjangoYekpayConfig',
        ...
    )

add  YEKPAY_MERCHANT_ID and YEKPAY_CALLBACK_URL with your data in the settings.py
Usage
----------
to use this module first get the information data from user and save it as a dict like this:
.. code-block:: python

  data = {
        "amount": 1000,
        "description": "some plan",
        "fromCurrencyCode": 364, #you can change this to then currency you want
        "toCurrencyCode": 364, #you can change this to then currency you want
        "firstName": 'example',
        "lastName": "example",
        "email": "ex@example.com",
        "mobile": "+4455884976",
        "address": "somewhere",
        "country": "Unaited Arab Emirates",
        "postalCode": "64976",
        "city": "Dubai",
}
use the function yekpay_start_transaction(data) to start the transation and user will be redirected to yekpay's gateway and after completing
transation yekpay will redirect to transation yekpay will redirect to YEKPAY_CALLBACK_URL you defined in setting.py earlier
after that you can call the method yekpay_proccess_transaction(request) to verify if transation was successful or not in case of success it
will return True and for fails it will return False(you can check terminal logs to see the error) and if there was something wrong with the payment it will return 'there was a problem in payment'
(again, you can check terminal logs for error).after all the row for this transaction will be verified in the database.

Features
--------

* easily multi currency transaction in django

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
