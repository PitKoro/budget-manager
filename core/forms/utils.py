from core.models import Account, ExpenseCategory, IncomeCategory


def get_account_choices():
    account_choices = []

    for account in Account.objects.all():
        account_choices.append(('acc__' + str(account.id), account.name))

    return account_choices


def get_income_category_choices():
    category_choices = []

    for category in IncomeCategory.objects.all():
        category_choices.append(('cat__' + str(category.id), category.name))

    return category_choices


def get_expense_category_choices():
    category_choices = []

    for category in ExpenseCategory.objects.all():
        category_choices.append(('cat__' + str(category.id), category.name))

    return category_choices
