=====
Usage
=====

To use Django yekpay in a project, add it to your `INSTALLED_APPS`:

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
