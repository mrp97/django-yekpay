# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect

from .models import Transaction
from .utils import generate_random_authority

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

# class transactionsDetailView(DetailView):
#     model = transactions
#
#
# class transactionsListView(ListView):
#     model = transactions
