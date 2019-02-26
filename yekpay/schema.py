import graphene
import django_filters
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Transaction


class TransactionNode(DjangoObjectType):
    class Meta:
        model = Transaction
        exclude_fields = ("authority_start", "authority_verify")
        interfaces = (relay.Node,)


class TransactionFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr="icontains")
    order_number = django_filters.CharFilter(lookup_expr="icontains")
    created_at_after = django_filters.DateFilter(
        field_name="created_at", lookup_expr="gt"
    )
    created_at_before = django_filters.DateFilter(
        field_name="created_at", lookup_expr="lt"
    )
    successful_payment_date_time_after = django_filters.DateFilter(
        field_name="successful_payment_date_time", lookup_expr="gt"
    )
    successful_payment_date_time_before = django_filters.DateFilter(
        field_name="successful_payment_date_time", lookup_expr="lt"
    )
    failure_reason = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Transaction
        fields = ["status", "order_number", "failure_reason"]

    @property
    def qs(self):
        return super().qs.filter(user=self.request.user)


class YekpayQuery:
    transactions = DjangoFilterConnectionField(
        TransactionNode, filterset_class=TransactionFilter
    )


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
