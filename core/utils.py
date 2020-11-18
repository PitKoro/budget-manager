from django.db.models import Sum
from django.db.models.functions import Coalesce
from .models import Account, IncomeCategory, IncomeTransaction, InnerTransaction, ExpenseCategory, ExpenseTransaction
import re

from functools import reduce
from itertools import chain
from operator import attrgetter

import datetime


def get_balance(account, date_to=datetime.date.today()):
    outer_income = account.incometransaction_set.filter(
        date__lte=date_to
    ).aggregate(
        amount=Coalesce(Sum('amount'), 0)
    )['amount']

    inner_income = account.inner_transaction_to_set.filter(
        date__lte=date_to
    ).aggregate(
        amount=Coalesce(Sum('amount'), 0)
    )['amount']

    outer_expense = account.expensetransaction_set.filter(
        date__lte=date_to
    ).aggregate(
        amount=Coalesce(Sum('amount'), 0)
    )['amount']

    inner_expense = account.inner_transaction_from_set.filter(
        date__lte=date_to
    ).aggregate(
        amount=Coalesce(Sum('amount'), 0)
    )['amount']

    return outer_income + inner_income - outer_expense - inner_expense


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

# Получение всех месяцев и годов существующих транзакций
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

# Получение всех категорий дохода в существующих транзакциях
def get_income_categories():
    incomeT = IncomeTransaction.objects.all()
    incomeCategoriesDict = {    "income filter inner": "Внутренние переводы",
                                0: "Все зачисления"}

    for el in incomeT:
        incomeCategoriesDict.update({el.income_category.id: el.income_category.name})
    
    return incomeCategoriesDict

# Получение всех категорий расхода в существующих транзакциях
def get_expense_categories():
    expenseT = ExpenseTransaction.objects.all()
    expenseCategoriesDict = {   "expense filter inner": "Внутренние переводы",
                                0: "Все расходы"}

    for el in expenseT:
        expenseCategoriesDict.update({el.expense_category.id: el.expense_category.name})
    
    return expenseCategoriesDict

# Получение всех чисел из строки
def find_nums_in_str(s):
    nums = re.findall(r'\d+', s)
    nums = [int(i) for i in nums]
    return nums

# Получение всех существующих транзакций с учетом фильтра по месяцам и годам
def get_all_transaction_with_month_and_year_filter(year_filter, month_filter):
    incomeT = IncomeTransaction.objects.filter(date__year=year_filter).filter(date__month=month_filter)
    expenseT = ExpenseTransaction.objects.filter(date__year=year_filter).filter(date__month=month_filter)
    innerT = InnerTransaction.objects.filter(date__year=year_filter).filter(date__month=month_filter)
    transactions = sorted((chain(incomeT, expenseT, innerT)), key=attrgetter('date'), reverse=True)
    return transactions

# Получение всех внутренних транзакций с учетом фильтра по месяцам и годам
def get_inner_transaction_with_month_and_year_filter(year_filter, month_filter):
    innerT = InnerTransaction.objects.filter(date__year=year_filter).filter(date__month=month_filter)
    transactions = sorted(innerT, key=attrgetter('date'), reverse=True)
    return transactions

# Получение всех транзакций дохода с учетом фильтра по месяцам и годам
def get_income_transaction_with_month_and_year_filter(year_filter, month_filter):
    incomeT = IncomeTransaction.objects.filter(date__year=year_filter).filter(date__month=month_filter)
    transactions = sorted(incomeT, key=attrgetter('date'), reverse=True)
    return transactions

# Получение всех транзакций дохода с учетом фильтра по месяцам и годам и фильтра по категориям
def get_income_transaction_with_month_and_year_filter_and_category_filter(year_filter, month_filter, income_category):
    incomeT = IncomeTransaction.objects.filter(date__year=year_filter).filter(date__month=month_filter).filter(income_category_id=income_category)
    transactions = sorted(incomeT, key=attrgetter('date'), reverse=True)
    return transactions

# Получение всех транзакций расхода с учетом фильтра по месяцам и годам
def get_expense_transaction_with_month_and_year_filter(year_filter, month_filter):
    expenseT = ExpenseTransaction.objects.filter(date__year=year_filter).filter(date__month=month_filter)
    transactions = sorted(expenseT, key=attrgetter('date'), reverse=True)
    return transactions

# Получение всех транзакций расхода с учетом фильтра по месяцам и годам и фильтра по категориям
def get_expense_transaction_with_month_and_year_filter_and_category_filter(year_filter, month_filter, expense_category):
    expenseT = ExpenseTransaction.objects.filter(date__year=year_filter).filter(date__month=month_filter).filter(expense_category_id=expense_category)
    transactions = sorted(expenseT, key=attrgetter('date'), reverse=True)
    return transactions

# Удвление транзакции дохода
def delete_income_transaction(POST_value):
    IncomeTransactionId=int(POST_value)
    IncomeTransaction.objects.filter(id=IncomeTransactionId).delete()

# Удвление транзакции расхода
def delete_expense_transaction(POST_value):
    ExpenseTransactionId=int(POST_value)
    ExpenseTransaction.objects.filter(id=ExpenseTransactionId).delete()

# Удвление внутренней транзакции
def delete_inner_transaction(POST_value):
    InnerTransactionId=int(POST_value)
    InnerTransaction.objects.filter(id=InnerTransactionId).delete()

# Удаление транзакции в зависимости от полученного POST запроса
def delete_transaction(request, POST_value):
    if POST_value == request.POST.get('IncomeTransactionId'):
        delete_income_transaction(POST_value)
    if POST_value == request.POST.get('ExpenseTransactionId'):
        delete_expense_transaction(POST_value)
    if POST_value == request.POST.get('InnerTransactionId'):
        delete_inner_transaction(POST_value)

# Получение значения фильтра по месяцам и годам в виде пары [month, year]
def get_month_year_filter(POST_value):
    month_year_filter = POST_value
    month_year_filter = find_nums_in_str(month_year_filter)
    return month_year_filter

def get_account_list():
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

    return account_list


def get_transactions_for_period(date_from, date_to):
    income_transactions = IncomeTransaction.objects.filter(
        date__range=[date_from, date_to]
    )
    expense_transactions = ExpenseTransaction.objects.filter(
        date__range=[date_from, date_to]
    )
    inner_transactions = InnerTransaction.objects.filter(
        date__range=[date_from, date_to]
    )

    tran_list = sorted(
        (chain(income_transactions, expense_transactions, inner_transactions)),
        key=attrgetter('date'),
        reverse=True
    )

    result = []
    for transaction in tran_list:
        type_name = ''
        from_name = ''
        to_name = ''

        if isinstance(transaction, IncomeTransaction):
            type_name = 'income'
            from_name = transaction.income_category.name
            to_name = transaction.account.name
        elif isinstance(transaction, ExpenseTransaction):
            type_name = 'expense'
            from_name = transaction.account.name
            to_name = transaction.expense_category.name
        elif isinstance(transaction, InnerTransaction):
            type_name = 'inner'
            from_name = transaction.account_from.name
            to_name = transaction.account_to.name

        result.append({
            'type': type_name,
            'date': transaction.date,
            'amount': transaction.amount / 100,
            'from': from_name,
            'to': to_name,
            'commentary': transaction.commentary
        })

    return result


def get_current_week_transactions():
    date_to = datetime.date.today()
    date_from = date_to - datetime.timedelta(days=date_to.weekday())

    return get_transactions_for_period(date_from, date_to)


def get_expenses_for_this_month():
    today = datetime.date.today()
    transactions = ExpenseTransaction.objects.values(
        'expense_category__name'
    ).filter(
        date__range=[datetime.date(today.year, today.month, 1), today]
    ).annotate(
        Sum('amount')
    )

    return list(map(
        lambda item: {
            'name': item['expense_category__name'],
            'amount': item['amount__sum'] / 100
        },
        transactions
    ))


def get_expenses_for_filter_month(month_filter, year_filter):
    transactions = ExpenseTransaction.objects.values(
        'expense_category__name'
    ).filter(date__year=year_filter).filter(date__month=month_filter).annotate(
        Sum('amount')
    )

    return list(map(
        lambda item: {
            'name': item['expense_category__name'],
            'amount': item['amount__sum'] / 100
        },
        transactions
    ))


def get_incomes_for_filter_month(month_filter, year_filter):
    transactions = IncomeTransaction.objects.values(
        'income_category__name'
    ).filter(date__year=year_filter).filter(date__month=month_filter).annotate(
        Sum('amount')
    )

    return list(map(
        lambda item: {
            'name': item['income_category__name'],
            'amount': item['amount__sum'] / 100
        },
        transactions
    ))