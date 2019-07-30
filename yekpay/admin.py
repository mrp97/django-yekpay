from django.contrib import admin
from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "email",
        "status",
        "amount",
        "successful_payment_date_time",
    ]


admin.site.register(Transaction, TransactionAdmin)

