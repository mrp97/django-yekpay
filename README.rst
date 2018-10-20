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

Add Django yekpay's URL patterns:

.. code-block:: python

    from django_yekpay import urls as django_yekpay_urls


    urlpatterns = [
        ...
        url(r'^', include(django_yekpay_urls)),
        ...
    ]

Features
--------

* TODO

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
