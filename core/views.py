from django.shortcuts import render
from itertools import chain
from operator import attrgetter
from .models import Account, IncomeTransaction, ExpenseTransaction, InnerTransaction
from .forms.IncomeForm import IncomeForm
from .forms.ExpenseForm import ExpenseForm 
from .utils import get_balance, post_income_transaction, post_expense_transaction
from functools import reduce


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

    return render(request, 'core/main.html', {
        'account_list': account_list,
        'url_name': url_name,
        'income_form': formIF,
        'expence_form': formEF
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
