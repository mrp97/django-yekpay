import graphene
from graphene_django import DjangoObjectType
from .models import Transaction
from graphene import InputObjectType
from .helpers import yekpay_start_transaction
from .exceptions import CallbackUrlNotProvided

class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction


class UserFields(graphene.AbstractType):
    firstName = graphene.String(required=False)
    lastName = graphene.String(required=False)
    email = graphene.String(required=False)
    mobile = graphene.String(required=False)


class AddressFields(graphene.AbstractType):
    address = graphene.String(required=False)
    country = graphene.String(required=False)
    postalCode = graphene.String(required=False)
    city = graphene.String(required=False)

class TransactionCreateInput(InputObjectType):
    amount = graphene.Int(required=False)
    description = graphene.String(required=False)
    fromCurrencyCode = graphene.String(required=False)
    toCurrencyCode = graphene.String(required=False)
    user = graphene.Field(UserFields)
    address = graphene.Field(AddressFields)


class CreateTransaction(graphene.ClientIDMutation):
    class Arguments:
        transaction_input = TransactionCreateInput
    redirect_url = graphene.String(required=True)

    def mutate_and_get_payload(self, info, transaction_input):
        redirect_url = yekpay_start_transaction(**transaction_input)
        return CreateTransaction(redirect_url=redirect_url)
