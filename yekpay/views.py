# -*- coding: utf-8 -*-
import random

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Transaction
from .utils import generate_random_authority, process_transaction_trans_status
from .request_utils import request_yekpay_verify, request_yekpay_verify_simulation
from .config import YEKPAY_SIMULATION, MERCHANTID, FAILURE_REASONS
from . import signals as yekpay_signals


def sandbox_pay(request, authority_start):
    if request.method == "GET":
        return render(request, "yekpay/sand-box.html")
    elif request.method == "POST":
        transaction = Transaction.objects.get(authority_start=authority_start)
        transaction_status = request.POST["status"]
        if transaction_status == "SUCCESS":
            transaction.success()
        elif transaction_status == "FAILED":
            random_failure_reason = FAILURE_REASONS[
                random.randint(0, len(FAILURE_REASONS)-1)
            ]
            transaction.fail(random_failure_reason)
        transaction.authority_verify = generate_random_authority()
        transaction.save(update_fields=["authority_verify"])
        return redirect(transaction.get_verify_url())


@csrf_exempt
def verify_transaction_view(
    request,
    transaction_order_number,
    request_function=request_yekpay_verify
):
    if YEKPAY_SIMULATION:
        request_function = request_yekpay_verify_simulation
    transaction = get_object_or_404(Transaction, order_number=transaction_order_number)
    trans_status = request_function(
        data={"merchantId": MERCHANTID, "authority": request.GET["authority"]}
    )
    transaction = process_transaction_trans_status(transaction, trans_status)
    yekpay_signals.transaction_verified.send(sender=None, transaction=transaction)
    return redirect(transaction.get_client_callback_url())
