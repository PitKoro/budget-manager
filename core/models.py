from django.db import models


class IncomeCategory(models.Model):
    name = models.CharField(max_length=100)


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)


class Account(models.Model):
    name = models.CharField(max_length=100)


class Transaction(models.Model):
    amount = models.PositiveIntegerField()
    date = models.DateField()
    commentary = models.TextField(blank=True)

    class Meta:
        abstract = True


class IncomeTransaction(Transaction):
    income_category = models.ForeignKey(IncomeCategory, on_delete=models.PROTECT)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)


class ExpenseTransaction(Transaction):
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    expense_category = models.ForeignKey(ExpenseCategory, on_delete=models.PROTECT)


class InnerTransaction(Transaction):
    account_from = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='inner_transaction_from_set')
    account_to = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='inner_transaction_to_set')
