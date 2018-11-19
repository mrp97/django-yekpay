import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Transaction
from graphene import InputObjectType, relay
from .helpers import yekpay_start_transaction
from .request_utils import request_yekpay_start_simulation

class TransactionNode(DjangoObjectType):
    class Meta:
        model = Transaction
        filter_fields = ['orderNumber']
        interfaces =(relay.Node,)


class Query(graphene.ObjectType):
    transaction = relay.node(TransactionNode)
    all_transactions = DjangoFilterConnectionField(TransactionNode)


class UserFields(graphene.InputObjectType):
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    email = graphene.String(required=True)
    mobile = graphene.String(required=True)


class AddressFields(graphene.InputObjectType):
    address = graphene.String(required=True)
    country = graphene.String(required=True)
    postal_node = graphene.String(required=True)
    city = graphene.String(required=True)

class TransactionCreateInput(graphene.InputObjectType):
    callback_url = graphene.String(required=False)
    amount = graphene.Int(required=True)
    description = graphene.String(required=True)
    fromCurrencyCode = graphene.String(required=True)
    toCurrencyCode = graphene.String(required=True)


class CreateTransaction(graphene.ClientIDMutation):
    class Arguments:
        transaction_input = TransactionCreateInput
        person_input = graphene.Field(UserFields)
        address_input = graphene.Field(AddressFields)
        simulation = graphene.Boolean(required=False)
    redirect_url = graphene.String(required=True)
    order_number = graphene.Int(required=True)

    @staticmethod
    def mutate(self, info, transaction_input, person_input,address_input, simulation):
        if simulation is not False:
            transaction = yekpay_start_transaction(
                request_function=request_yekpay_start_simulation,

                **transaction_input
            )
        else:
            transaction = yekpay_start_transaction(**transaction_input)
        return CreateTransaction(
            redirect_url=transaction.get_transaction_start_url(),
            order_number=transaction.orderNumber.hashid
        )
