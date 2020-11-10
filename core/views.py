from django.shortcuts import render
<<<<<<< HEAD
from .models import Account, IncomeTransaction, ExpenseTransaction, InnerTransaction
from .forms.IncomeForm import IncomeForm
from .forms.ExpenseForm import ExpenseForm

import core.utils as utils

from .utils import get_balance, post_income_transaction, post_expense_transaction, get_expenses

from functools import reduce
from itertools import chain
from operator import attrgetter

import datetime
=======
from .models import IncomeTransaction, ExpenseTransaction, InnerTransaction
from .forms.IncomeForm import IncomeForm
from .forms.ExpenseForm import ExpenseForm
import core.utils as utils

from itertools import chain
from operator import attrgetter
>>>>>>> master


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
<<<<<<< HEAD
            visible_form = 'expense'
            if formEF.is_valid():
                utils.post_expense_transaction(formEF.cleaned_data)
                formEF = ExpenseForm()

    url_name = request.resolver_match.url_name
    account_list = []

    for account in Account.objects.all():
        account_list.append({
            'name': account.name,
            'amount': utils.get_balance(account)/100
        })
    account_list.insert(0, {
        'name': 'Всего',
        'amount': reduce(
            lambda acc, value: acc + value['amount'],
            account_list,
            0
        )
    })
=======

        if formIF.is_valid():
            utils.post_income_transaction(formIF.cleaned_data)
            formIF = IncomeForm()
        if formEF.is_valid():
            utils.post_expense_transaction(formEF.cleaned_data)
            formEF = ExpenseForm()

    url_name = request.resolver_match.url_name
>>>>>>> master

    

    expenses = utils.get_expenses()

    return render(request, 'core/main.html', {
        'account_list': utils.get_account_list(),
        'latest_transactions': utils.get_current_week_transactions(),
        'url_name': url_name,
        'income_form': formIF,
        'expence_form': formEF,
        # 'expense_chart_data': utils.get_data_for_expense_diagram()
        'expense_chart_data': utils.get_data_for_expense_diagram(),
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
