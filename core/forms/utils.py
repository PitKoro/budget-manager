from core.models import Account, ExpenseCategory, IncomeCategory



def get_account_choices():
    account_choices = []

    for account in Account.objects.all():
        account_choices.append(('acc__' + str(account.id), account.name))

    return account_choices


def get_category_choices(cat="inc_c"):
    category_choices = []

    if cat == "inc_c":
        for category in IncomeCategory.objects.all():
            category_choices.append(('cat__' + str(category.id), category.name))
    elif cat == "exp_c":
        for category in ExpenseCategory.objects.all():
            category_choices.append(('cat__' + str(category.id), category.name))

    return category_choices