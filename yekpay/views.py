# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect

from .models import Transaction
from .utils import generate_random_authority
from .helpers import yekpay_process_transaction


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


def verify_transaction_view(request):
    transaction = yekpay_process_transaction(request)
    url = ""
    order_number=int(request.GET.get('orderNo'))
    if transaction is None:
        transaction = Transaction.objects.get(order_number=order_number)
    return redirect(url+'?on='+str(transaction.orderNumber.hash_id))

# class transactionsDetailView(DetailView):
#     model = transactions
#
#
# class transactionsListView(ListView):
#     model = transactions
