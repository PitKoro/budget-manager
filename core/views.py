from django.shortcuts import render
from .models import Account, IncomeTransaction, ExpenseTransaction, InnerTransaction
from .forms.IncomeForm import IncomeForm
from .forms.ExpenseForm import ExpenseForm

import core.utils as utils

from functools import reduce
from itertools import chain
from operator import attrgetter


def main(request):
    visible_form = 'expense'

    # Обработка формы
    formEF = ExpenseForm()
    formIF = IncomeForm()
    if request.method == 'POST':
        if request.POST['form'] == "incf":
            formIF = IncomeForm(request.POST)
            visible_form = 'income'

            if formIF.is_valid():
                utils.post_income_transaction(formIF.cleaned_data)
                formIF = IncomeForm()
        elif request.POST['form'] == "expf":
            formEF = ExpenseForm(request.POST)
            visible_form = 'expense'
            if formEF.is_valid():
                utils.post_expense_transaction(formEF.cleaned_data)
                formEF = ExpenseForm()

    url_name = request.resolver_match.url_name

    expenses = utils.get_expenses_for_this_month()

    return render(request, 'core/main.html', {
        'account_list': utils.get_account_list(),
        'latest_transactions': utils.get_current_week_transactions(),
        'url_name': url_name,
        'income_form': formIF,
        'expence_form': formEF,
        'expense_chart_data': utils.get_expenses_for_this_month(),
        'visible_form': visible_form,
        'expenses': expenses
    })


def report(request):
    url_name = request.resolver_match.url_name
    return render(request, 'core/report.html', {'url_name': url_name})


def history(request):
    url_name = request.resolver_match.url_name

    filter_value = "all"

    if request.method == 'POST':
        if request.POST.get('history_filter'):
            filter_value=request.POST.get('history_filter')
            if filter_value == "all":
                incomeT = IncomeTransaction.objects.all()
                expenseT = ExpenseTransaction.objects.all()
                innerT = InnerTransaction.objects.all()
                transactions = sorted((chain(incomeT, expenseT, innerT)), key=attrgetter('date'), reverse=True)
                return render(request, 'core/history.html', {'url_name': url_name, 'transactions':transactions, 'filter_value': filter_value})
            if int(filter_value) in range(1,13):
                incomeT = IncomeTransaction.objects.filter(date__month=int(filter_value))
                expenseT = ExpenseTransaction.objects.filter(date__month=int(filter_value))
                innerT = InnerTransaction.objects.filter(date__month=int(filter_value))
                transactions = sorted((chain(incomeT, expenseT, innerT)), key=attrgetter('date'), reverse=True)
                return render(request, 'core/history.html', {'url_name': url_name, 'transactions': transactions, 'filter_value': filter_value})

        if request.POST.get('IncomeTransactionId'):
            IncomeTransactionId=int(request.POST.get('IncomeTransactionId'))
            IncomeTransaction.objects.filter(id=IncomeTransactionId).delete()
        
        if request.POST.get('InnerTransactionId'):
            InnerTransactionId=int(request.POST.get('InnerTransactionId'))
            InnerTransaction.objects.filter(id=InnerTransactionId).delete()

        if request.POST.get('ExpenseTransactionId'):
            ExpenseTransactionId=int(request.POST.get('ExpenseTransactionId'))
            ExpenseTransaction.objects.filter(id=ExpenseTransactionId).delete()
    incomeT = IncomeTransaction.objects.all()
    expenseT = ExpenseTransaction.objects.all()
    innerT = InnerTransaction.objects.all()
    transactions = sorted((chain(incomeT, expenseT, innerT)), key=attrgetter('date'), reverse=True)

    filter_value = "all"

    if request.method == 'POST':
        filter_value=request.POST.get('history_filter')
        if filter_value == "all":
            return render(request, 'core/history.html', {'url_name': url_name, 'transactions':transactions, 'filter_value': filter_value})
        if int(filter_value) in range(1,13):
            incomeT = IncomeTransaction.objects.filter(date__month=int(filter_value))
            expenseT = ExpenseTransaction.objects.filter(date__month=int(filter_value))
            innerT = InnerTransaction.objects.filter(date__month=int(filter_value))
            transactions = sorted((chain(incomeT, expenseT, innerT)), key=attrgetter('date'), reverse=True)
            return render(request, 'core/history.html', {'url_name': url_name, 'transactions':transactions, 'filter_value': filter_value})

    return render(request, 'core/history.html', {'url_name': url_name, 'transactions': transactions, 'filter_value': filter_value})
