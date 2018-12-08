import graphene
import django_filters
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .config import TRANSACTION_STATUS_CHIOCES
from .models import Transaction
from .helpers import yekpay_start_transaction
from .request_utils import request_yekpay_start_simulation


class TransactionNode(DjangoObjectType):
    class Meta:
        model = Transaction
        interfaces =(relay.Node,)

class TransactionFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr='icontains')
    order_number = django_filters.CharFilter(lookup_expr='icontains')
    created_at_after = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gt'
    )
    created_at_before = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='lt'
    )
    successful_payament_date_time_after = django_filters.DateFilter(
        field_name='successful_payament_date_time',
        lookup_expr='gt'
    )
    successful_payament_date_time_before = django_filters.DateFilter(
        field_name='successful_payament_date_time',
        lookup_expr='lt'
    )
    failure_reason = django_filters.CharFilter(lookup_expr='icontains')   

    class Meta:
        model = Transaction
        fields = [
            'status',
            'order_number',
            'failure_reason'
        ]

    @property
    def qs(self):
        return super().qs.filter(user=self.request.user)


class YekpayQuery():
    transactions = DjangoFilterConnectionField(TransactionNode, filterset_class=TransactionFilter)


class UserFields(graphene.InputObjectType):
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    email = graphene.String(required=True)
    mobile = graphene.String(required=True)


class AddressFields(graphene.InputObjectType):
    address = graphene.String(required=True)
    country = graphene.String(required=True)
    postal_code = graphene.String(required=True)
    city = graphene.String(required=True)


class TransactionFields(graphene.InputObjectType):
    callback_url = graphene.String(required=False)
    amount = graphene.Int(required=True)
    description = graphene.String(required=True)
    fromCurrencyCode = graphene.String(required=True)
    toCurrencyCode = graphene.String(required=True)


# class CreateTransaction(graphene.ClientIDMutation):
#     class Arguments:
#         transaction_input = graphene.Field(TransactionFields)
#         person_input = graphene.Field(UserFields)
#         address_input = graphene.Field(AddressFields)
#         simulation = graphene.Boolean(required=False)
#     redirect_url = graphene.String(required=True)
#     order_number = graphene.Int(required=True)

#     def mutate(self, info, transaction_input, person_input,address_input, simulation):
#         if simulation is not False:
#             transaction = yekpay_start_transaction(
#                 request_function=request_yekpay_start_simulation,
#                 **transaction_input
#             )
#         else:
#             transaction = yekpay_start_transaction(**transaction_input)
#         # get user info
#         return CreateTransaction(
#             redirect_url=transaction.get_transaction_start_url(),
#             order_number=transaction.order_number.hashid
#         )
