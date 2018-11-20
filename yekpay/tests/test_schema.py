import graphene
from graphene.test import Client
from snapshottest.django import TestCase
from .. import (schema, models, helpers)
from . import test_data


from django.contrib.auth.models import User
class Query(schema.Query, graphene.ObjectType):
    pass

sample_schema = graphene.Schema(query=Query)

class YekpayAPITestCase(TestCase):
    def create_transaction_with_wrong__data(self):
        client = Client(sample_schema)
        self.assertMatchSnapshot(client.execute(''''''))

    def verify_transaction(self):
        client = Client(sample_schema)
        result = client.execute('''''')
        self.assertMatchSnapshot(result)
        transaction = models.Transaction.objects.get(orderNumber=result.get('order_number'))
        transaction.status = 'SUCCESS'
        self.assertMatchSnapshot(client.execute(''''''))



