from django.db.models import Sum
from django.db.models.functions import Coalesce
from .models import Account, IncomeCategory, IncomeTransaction, InnerTransaction, ExpenseCategory, ExpenseTransaction
from itertools import chain


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
        monthList.append(el.date.month)

    monthList.sort()
    monthDict = {}
    
    for i in range(0, len(monthList)):
        if monthList[i] == 1:
            monthDict.update({1: 'Январь'})
        if monthList[i] == 2:
            monthDict.update({2: 'Февраль'})
        if monthList[i] == 3:
            monthDict.update({3: 'Март'})
        if monthList[i] == 4:
            monthDict.update({4: 'Апрель'})
        if monthList[i] == 5:
            monthDict.update({5: 'Май'})
        if monthList[i] == 6:
            monthDict.update({6: 'Июнь'})
        if monthList[i] == 7:
            monthDict.update({7: 'Июль'})
        if monthList[i] == 8:
            monthDict.update({8: 'Август'})
        if monthList[i] == 9:
            monthDict.update({9: 'Сентябрь'})
        if monthList[i] == 10:
            monthDict.update({10: 'Октябрь'})
        if monthList[i] == 11:
            monthDict.update({11: 'Ноябрь'})
        if monthList[i] == 12:
            monthDict.update({12: 'Декабрь'})
        
    return monthDict