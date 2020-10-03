from django.db import models


class IncomeCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'core_income_category'


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'core_expense_category'


class Account(models.Model):
    name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
