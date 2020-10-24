from django.db.models import Sum
from django.db.models.functions import Coalesce
from .models import Account, IncomeCategory, IncomeTransaction, InnerTransaction


def get_balance(account):
    outer_income = account.incometransaction_set.aggregate(amount=Coalesce(Sum('amount'), 0))['amount']
    inner_income = account.inner_transaction_to_set.aggregate(amount=Coalesce(Sum('amount'), 0))['amount']
    outer_expense = account.expensetransaction_set.aggregate(amount=Coalesce(Sum('amount'), 0))['amount']
    inner_expense = account.inner_transaction_from_set.aggregate(amount=Coalesce(Sum('amount'), 0))['amount']

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
