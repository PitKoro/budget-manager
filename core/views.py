from django.shortcuts import render
from .models import Account, IncomeTransaction, ExpenseTransaction, InnerTransaction
from .forms.IncomeForm import IncomeForm
from .forms.ExpenseForm import ExpenseForm
from .utils import get_balance, post_income_transaction, post_expense_transaction, get_expenses

from functools import reduce
from itertools import chain
from operator import attrgetter


def main(request):
    # Обработка формы
    formEF = ExpenseForm()
    formIF = IncomeForm()
    if request.method == 'POST':
        if request.POST['form'] == "incf":
            formIF = IncomeForm(request.POST)
        elif request.POST['form'] == "expf":
            formEF = ExpenseForm(request.POST)

        if formIF.is_valid():
            post_income_transaction(formIF.cleaned_data)
            formIF = IncomeForm()
        if formEF.is_valid():
            post_expense_transaction(formEF.cleaned_data)
            formEF = ExpenseForm()

    url_name = request.resolver_match.url_name
    account_list = []

    for account in Account.objects.all():
        account_list.append({
            'name': account.name,
            'amount': get_balance(account)/100
        })
    account_list.insert(0, {
        'name': 'Всего',
        'amount': reduce(
            lambda acc, value: acc + value['amount'],
            account_list,
            0
        )
    })

    expenses = get_expenses()

    return render(request, 'core/main.html', {
        'account_list': account_list,
        'url_name': url_name,
        'income_form': formIF,
        'expence_form': formEF,
        'expenses': expenses
    })


def report(request):
    url_name = request.resolver_match.url_name
    return render(request, 'core/report.html', {'url_name': url_name})


def history(request):
    url_name = request.resolver_match.url_name
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
