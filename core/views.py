from django.shortcuts import render
from .models import IncomeTransaction, ExpenseTransaction, InnerTransaction
from .forms.IncomeForm import IncomeForm
from .forms.ExpenseForm import ExpenseForm

import core.utils as utils

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

    return render(request, 'core/main.html', {
        'account_list': utils.get_account_list(),
        'latest_transactions': utils.get_current_week_transactions(),
        'url_name': url_name,
        'income_form': formIF,
        'expence_form': formEF,
        'visible_form': visible_form,
        'expenses': utils.get_expenses_for_this_month()
    })


def report(request):
    url_name = request.resolver_match.url_name
    income_transaction_list = []
    for income in IncomeTransaction.objects.all():
        income_transaction_list.append(income.amount)
    print(income_transaction_list)
    income_summ = sum(income_transaction_list)
    expense_transaction_list = []
    for expense in ExpenseTransaction.objects.all():
        expense_transaction_list.append(expense.amount)
    expense_summ = sum(expense_transaction_list)

    expense_category_amount_list1 = []
    for el in ExpenseTransaction.objects.filter(expense_category_id=1):
        expense_category_amount_list1.append(el.amount)
    expense_category_amount_summ1=sum(expense_category_amount_list1)

    expense_category_amount_list2 = []
    for el in ExpenseTransaction.objects.filter(expense_category_id=2):
        expense_category_amount_list2.append(el.amount)
    expense_category_amount_summ2=sum(expense_category_amount_list2)
    
    expense_category_amount_list3 = []
    for el in ExpenseTransaction.objects.filter(expense_category_id=3):
        expense_category_amount_list3.append(el.amount)
    expense_category_amount_summ3=sum(expense_category_amount_list3)

    expense_category_amount_list4 = []
    for el in ExpenseTransaction.objects.filter(expense_category_id=4):
        expense_category_amount_list4.append(el.amount)
    expense_category_amount_summ4=sum(expense_category_amount_list4)

    income_category_amount_list1 = []
    for el in IncomeTransaction.objects.filter(income_category_id=1):
        income_category_amount_list1.append(el.amount)
    income_category_amount_summ1=sum(income_category_amount_list1)

    income_category_amount_list2 = []
    for el in IncomeTransaction.objects.filter(income_category_id=2):
        income_category_amount_list2.append(el.amount)
    income_category_amount_summ2=sum(income_category_amount_list2)

    income_category_amount_list3 = []
    for el in IncomeTransaction.objects.filter(income_category_id=3):
        income_category_amount_list3.append(el.amount)
    income_category_amount_summ3=sum(income_category_amount_list3)
    
    

    return render(request, 'core/report.html', {'url_name': url_name, 
                                                'income_summ': income_summ, 
                                                'expense_summ': expense_summ,
                                                'expense_category_amount_summ1': expense_category_amount_summ1,
                                                'expense_category_amount_summ2': expense_category_amount_summ2,
                                                'expense_category_amount_summ3': expense_category_amount_summ3,
                                                'expense_category_amount_summ4': expense_category_amount_summ4,
                                                'income_category_amount_summ1': income_category_amount_summ1,
                                                'income_category_amount_summ2': income_category_amount_summ2,
                                                'income_category_amount_summ3': income_category_amount_summ3})


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
