from core.models import Account, IncomeCategory, ExpenseCategory

import json

with open('data.json', 'r') as file:
    data = json.load(file)

for acc in data['account']:
    account = Account(name=acc['name'])
    account.save()

for in_c in data['incomeCategory']:
    incomeCategory = IncomeCategory(name=in_c['name'])
    incomeCategory.save()

for ex_c in data['expenseCategory']:
    expenseCategory = ExpenseCategory(name=ex_c['name'])
    expenseCategory.save()
