from django.db.models import Sum
from django.db.models.functions import Coalesce
from .models import Account, IncomeCategory, IncomeTransaction, InnerTransaction, ExpenseCategory, ExpenseTransaction

from datetime import date


def get_balance(account, date_to=date.today()):
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


def get_expenses(date_to=date.today()):
    expenses_dic = {}
    month_date = date(date_to.year, date_to.month, 1)
    for cat in ExpenseCategory.objects.all():
        expenses_dic[cat.name] = ExpenseTransaction.objects.filter(
                expense_category_id=cat.id
        ).filter(
                date__lte=date_to
        ).filter(
                date__gte=month_date
        ).aggregate(
                amount=Coalesce(Sum('amount'), 0)
        )['amount']/100
    expenses_arr = []
    for name, value in expenses_dic.items():
        expenses_arr.append({
            'name': name, 
            'value': value
        })
    return expenses_arr