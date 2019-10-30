import graphene
from graphene.test import Client
from snapshottest.django import TestCase
from .. import schema, models, helpers
from .test_data import transaction_data, transaction_wrong_data

from django.contrib.auth.models import User


class Query(schema.YekpayQuery, graphene.ObjectType):
    pass


sample_schema = graphene.Schema(query=Query)


class YekpayAPITestCase(TestCase):
    def create_transaction_with_wrong__data(self):
        client = Client(sample_schema)
        self.assertMatchSnapshot(
            client.execute(
                """
            mutation CreateTransaction ($amount: Float!, $description: String!, from_currency_code: String!, to_currency_code: String!, first_name: String!, last_name: String!, email: String!, mobile: String!, address: String!, country: String!, postal_code: String!, city: String!){
                  createTransaction(amount: $amount, description: $description, fromCurrencyCode: $from_currency_code ,toCurrencyCode: $to_currency_code, firstName: $first_name, lastName: $last_name, mobile: $mobile, address: $address, country: $country, postal_code: $postal_code, city: $city) {
                    redirect_url
                    order_number
              }
            }
        """
            ),
            transaction_wrong_data,
        )

    def verify_transaction(self):
        client = Client(sample_schema)
        result = client.execute(
            """
            mutation CreateTransaction ($amount: Float!, $description: String!, from_currency_code: String!, to_currency_code: String!, first_name: String!, last_name: String!, email: String!, mobile: String!, address: String!, country: String!, postal_code: String!, city: String!){
                  createTransaction(amount: $amount, description: $description, fromCurrencyCode: $from_currency_code ,toCurrencyCode: $to_currency_code, firstName: $first_name, lastName: $last_name, mobile: $mobile, address: $address, country: $country, postal_code: $postal_code, city: $city) {
                    redirect_url
                    order_number
              }
            }
        """,
            transaction_data,
        )
        self.assertMatchSnapshot(result)
        transaction = models.Transaction.objects.get(
            order_number=result.get("order_number")
        )
        transaction.status = "SUCCESS"
        self.assertMatchSnapshot(
            client.execute(
                """
            query Transaction($orderNumber: ID!)
                allTransaction(orderNumber: $orderNumber) {
                    edges {
                        node {
                            status
                        }
                    }
                }
            """,
                f"""
            orderNumber: {result.get('order_number')}
            """,
            )
        )

