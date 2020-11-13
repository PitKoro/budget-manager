from django.db.models import Sum
from django.db.models.functions import Coalesce
from .models import Account, IncomeCategory, IncomeTransaction, InnerTransaction, ExpenseCategory, ExpenseTransaction
from itertools import chain
from operator import attrgetter
import re


def get_balance(account):
    outer_income = account.incometransaction_set.aggregate(
        amount=Coalesce(Sum('amount'), 0)
    )['amount']

    inner_income = account.inner_transaction_to_set.aggregate(
        amount=Coalesce(Sum('amount'), 0)
    )['amount']

    outer_expense = account.expensetransaction_set.aggregate(
        amount=Coalesce(Sum('amount'), 0)
    )['amount']

    inner_expense = account.inner_transaction_from_set.aggregate(
        amount=Coalesce(Sum('amount'), 0)
    )['amount']

    return (outer_income + inner_income - outer_expense - inner_expense)


def post_income_transaction(data):
    from_id = data['from1'].split('__')[1]
    to_id = data['to'].split('__')[1]
    amount = data['amount'] * 100

    transaction = None

    to = Account.objects.get(id=to_id)

    if (data['from1'].startswith('cat__')):
        transaction = IncomeTransaction(
            amount=amount,
            date=data['date'],
            commentary=data['commentary'],
            income_category=IncomeCategory.objects.get(id=from_id),
            account=to
        )
    else:
        transaction = InnerTransaction(
            amount=amount,
            date=data['date'],
            commentary=data['commentary'],
            account_from=Account.objects.get(id=from_id),
            account_to=to
        )

    transaction.save()


def post_expense_transaction(data):
    from_id = data['from_cat'].split('__')[1]
    to_id = data['to_cat'].split('__')[1]
    amount = data['amount_exp'] * 100

    transaction = None

    if data['to_cat'].startswith('cat__'):
        transaction = ExpenseTransaction(
            amount=amount,
            date=data['when'],
            commentary=data['commentary_exp'],
            account=Account.objects.get(id=from_id),
            expense_category=ExpenseCategory.objects.get(id=to_id)
        )
    else:
        transaction = InnerTransaction(
            amount=amount,
            date=data['when'],
            commentary=data['commentary_exp'],
            account_from=Account.objects.get(id=from_id),
            account_to=Account.objects.get(id=to_id)
        )
    transaction.save()


def get_month():
    incomeT = IncomeTransaction.objects.all()
    expenseT = ExpenseTransaction.objects.all()
    innerT = InnerTransaction.objects.all()
    transactions = chain(incomeT, expenseT, innerT)

    monthList = []

    for el in transactions:
        monthList.append((el.date.month, el.date.year))

    sorted(monthList, reverse=True)

    monthDict = {}
    
    for i in range(0, len(monthList)):
        if monthList[i][0] == 1:
            monthDict.update({(1, monthList[i][1]): 'Январь '+str(monthList[i][1])})
        if monthList[i][0] == 2:
            monthDict.update({(2, monthList[i][1]): 'Февраль '+str(monthList[i][1])})
        if monthList[i][0] == 3:
            monthDict.update({(3, monthList[i][1]): 'Март '+str(monthList[i][1])})
        if monthList[i][0] == 4:
            monthDict.update({(4, monthList[i][1]): 'Апрель '+str(monthList[i][1])})
        if monthList[i][0] == 5:
            monthDict.update({(5, monthList[i][1]): 'Май '+str(monthList[i][1])})
        if monthList[i][0] == 6:
            monthDict.update({(6, monthList[i][1]): 'Июнь '+str(monthList[i][1])})
        if monthList[i][0] == 7:
            monthDict.update({(7, monthList[i][1]): 'Июль '+str(monthList[i][1])})
        if monthList[i][0] == 8:
            monthDict.update({(8, monthList[i][1]): 'Август '+str(monthList[i][1])})
        if monthList[i][0] == 9:
            monthDict.update({(9, monthList[i][1]): 'Сентябрь '+str(monthList[i][1])})
        if monthList[i][0] == 10:
            monthDict.update({(10, monthList[i][1]): 'Октябрь '+str(monthList[i][1])})
        if monthList[i][0] == 11:
            monthDict.update({(11, monthList[i][1]): 'Ноябрь '+str(monthList[i][1])})
        if monthList[i][0] == 12:
            monthDict.update({(12, monthList[i][1]): 'Декабрь '+str(monthList[i][1])})        
    return monthDict

def get_income_categories():
    incomeT = IncomeTransaction.objects.all()
    incomeCategoriesDict = {    "income filter inner": "Внутренние переводы",
                                0: "Все зачисления"}

    for el in incomeT:
        incomeCategoriesDict.update({el.income_category.id: el.income_category.name})
    
    return incomeCategoriesDict

def get_expense_categories():
    expenseT = ExpenseTransaction.objects.all()
    expenseCategoriesDict = {   "expense filter inner": "Внутренние переводы",
                                0: "Все расходы"}

    for el in expenseT:
        expenseCategoriesDict.update({el.expense_category.id: el.expense_category.name})
    
    return expenseCategoriesDict


def find_nums_in_str(s):
    nums = re.findall(r'\d+', s)
    nums = [int(i) for i in nums]
    return nums


def get_all_transaction_with_month_and_year_filter(year_filter, month_filter):
    incomeT = IncomeTransaction.objects.filter(date__year=year_filter).filter(date__month=month_filter)
    expenseT = ExpenseTransaction.objects.filter(date__year=year_filter).filter(date__month=month_filter)
    innerT = InnerTransaction.objects.filter(date__year=year_filter).filter(date__month=month_filter)
    transactions = sorted((chain(incomeT, expenseT, innerT)), key=attrgetter('date'), reverse=True)
    return transactions


def get_inner_transaction_with_month_and_year_filter(year_filter, month_filter):
    innerT = InnerTransaction.objects.filter(date__year=year_filter).filter(date__month=month_filter)
    transactions = sorted(innerT, key=attrgetter('date'), reverse=True)
    return transactions


def get_income_transaction_with_month_and_year_filter(year_filter, month_filter):
    incomeT = IncomeTransaction.objects.filter(date__year=year_filter).filter(date__month=month_filter)
    transactions = sorted(incomeT, key=attrgetter('date'), reverse=True)
    return transactions


def get_income_transaction_with_month_and_year_filter_and_category_filter(year_filter, month_filter, income_category):
    incomeT = IncomeTransaction.objects.filter(date__year=year_filter).filter(date__month=month_filter).filter(income_category_id=income_category)
    transactions = sorted(incomeT, key=attrgetter('date'), reverse=True)
    return transactions


def get_expense_transaction_with_month_and_year_filter(year_filter, month_filter):
    expenseT = ExpenseTransaction.objects.filter(date__year=year_filter).filter(date__month=month_filter)
    transactions = sorted(expenseT, key=attrgetter('date'), reverse=True)
    return transactions


def get_expense_transaction_with_month_and_year_filter_and_category_filter(year_filter, month_filter, expense_category):
    expenseT = ExpenseTransaction.objects.filter(date__year=year_filter).filter(date__month=month_filter).filter(expense_category_id=expense_category)
    transactions = sorted(expenseT, key=attrgetter('date'), reverse=True)
    return transactions


def delete_income_transaction(POST_value):
    IncomeTransactionId=int(POST_value)
    IncomeTransaction.objects.filter(id=IncomeTransactionId).delete()


def delete_expense_transaction(POST_value):
    ExpenseTransactionId=int(POST_value)
    ExpenseTransaction.objects.filter(id=ExpenseTransactionId).delete()


def delete_inner_transaction(POST_value):
    InnerTransactionId=int(POST_value)
    InnerTransaction.objects.filter(id=InnerTransactionId).delete()


def delete_transaction(request, POST_value):
    if POST_value == request.POST.get('IncomeTransactionId'):
        delete_income_transaction(POST_value)
    if POST_value == request.POST.get('ExpenseTransactionId'):
        delete_expense_transaction(POST_value)
    if POST_value == request.POST.get('InnerTransactionId'):
        delete_inner_transaction(POST_value)


def get_month_year_filter(POST_value):
    month_year_filter = POST_value
    month_year_filter = find_nums_in_str(month_year_filter)
    return month_year_filter