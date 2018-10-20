# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
) 

from .models import (
	transactions,
)

def startTransaction(request):


class verifyTransaction(CreateView):

    model = transactions


class transactionsDetailView(DetailView):

    model = transactions


class transactionsListView(ListView):

    model = transactions
