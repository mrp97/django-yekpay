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
    search_fields = ("user__email", "user__first_name", "user__last_name")
    list_filter = ("status", "create_at", "successful_payment_date_time")


admin.site.register(Transaction, TransactionAdmin)
