from django.contrib import admin

from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "status",
        "amount",
        "created_at",
        "successful_payment_date_time",
        "failure_date_time",
    ]


admin.site.register(Transaction, TransactionAdmin)
