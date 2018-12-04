# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404

from .models import Transaction
from .utils import generate_random_authority, process_transaction_trans_status
from .helpers import yekpay_process_transaction
from .request_utils import request_yekpay_verify


def sandbox_pay(request, authority_start):
    if request.method == 'GET':
        return render(
            request,
            'yekpay/sand-box.html'
        )
    elif request.method == 'POST':
        transaction = Transaction.objects.get(authorityStart= authority_start)
        transaction.status = request.POST['status']
        transaction.authorityVerify = generate_random_authority()
        transaction.save(update_fields=['authorityVerify', 'status'])
        return redirect(f'{transaction.callback_url}?authority={transaction.authorityVerify}')


def verify_transaction_view(request,transaction_order_number,request_function=request_yekpay_verify):
    if YEKPAY_SIMULATION:
        request_function = request_yekpay_verify_simulation
    transaction = get_object_or_404(
        Transaction,
        order_number=transaction_order_number
    )
    trans_status = request_function(
        data=  {
            "merchantId": MERCHANTID,
            "authority": request.GET['authority']
        }
    )
    transaction = process_transaction_trans_status(
        transaction,
        trans_status
    )
    return redirect(transaction.get_client_callback_url())

# class transactionsDetailView(DetailView):
#     model = transactions
#
#
# class transactionsListView(ListView):
#     model = transactions
