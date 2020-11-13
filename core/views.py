from django.shortcuts import render
from .models import Account, IncomeTransaction, ExpenseTransaction, InnerTransaction
from .forms.IncomeForm import IncomeForm
from .forms.ExpenseForm import ExpenseForm 
import core.utils as utils
from functools import reduce
import datetime

def main(request):
    # Обработка формы
    formEF = ExpenseForm()
    formIF = IncomeForm()
    if request.method == 'POST':
        if request.POST['form'] == "incf":
            formIF = IncomeForm(request.POST)
        elif request.POST['form'] == "expf":
            formEF = ExpenseForm(request.POST)

        if formIF.is_valid():
            post_income_transaction(formIF.cleaned_data)
            formIF = IncomeForm()
        if formEF.is_valid():
            post_expense_transaction(formEF.cleaned_data)
            formEF = ExpenseForm()

    url_name = request.resolver_match.url_name
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

    return render(request, 'core/main.html', {
        'account_list': account_list,
        'url_name': url_name,
        'income_form': formIF,
        'expence_form': formEF
    })


def report(request):
    url_name = request.resolver_match.url_name
    return render(request, 'core/report.html', {'url_name': url_name})


def history(request):
    url_name = request.resolver_match.url_name # Получение имени активной страницы

    now = datetime.datetime.now()
    month_filter = now.month # Значение месяца по умолчанию для фильра по месяцу и году
    year_filter = now.year # Значение года по умолчанию для фильра по месяцу и году
    income_category = None # Значение фильтра по категориям дохода
    expense_category = None # Значение фильтра по категориям расхода

    if request.method == 'POST': # Если пользователь воспользовался любым фильтром или удалением транзакции

        if request.POST.get('IncomeTransactionId'): # Если пользователь воспользовался удалением транзакции дохода
            utils.delete_transaction(request, request.POST.get('IncomeTransactionId')) # Удаление транзакции дохода
    
        if request.POST.get('InnerTransactionId'): # Если пользователь воспользовался удалением внутренней транзакции 
            utils.delete_transaction(request, request.POST.get('InnerTransactionId')) # Удаление внутренней транзакции

        if request.POST.get('ExpenseTransactionId'): # Если пользователь воспользовался удалением транзакции расхода
            utils.delete_transaction(request, request.POST.get('ExpenseTransactionId')) # Удаление транзакции расхода

        if request.POST.get('month_filter_history'): # Если пользователь применил фильтр по месяцу и году
            month_year_filter = utils.get_month_year_filter(request.POST.get('month_filter_history')) # Получение значения фильтра по месяцам и годам в виде пары (month, year)
            month_filter = month_year_filter[0] # Получение значения месяца из пары (month, year)
            year_filter = month_year_filter[1] # Получение значения года из пары (month, year)

            if request.POST.get('income_filter_history') == 'income filter inner': # Если в фильтре категориях дохода выбрано значение "Внутренние переводы"
                expense_category = None
                income_category = request.POST.get('income_filter_history') # Получение значения фильтра по категориям дохода
                transactions = utils.get_inner_transaction_with_month_and_year_filter(year_filter, month_filter) # Получение всех внутренних транзакций с учетом фильтра по месяцам и годам

                monthDict = get_month() # Получение всех месяцев и годов существующих транзакций
                incomeCategoriesDict = utils.get_income_categories() # Получение всех категорий дохода в существующих транзакциях
                expenseCategoriesDict = utils.get_expense_categories() # Получение всех категорий расхода в существующих транзакциях

                return render(
                                request, 'core/history.html',
                                {'url_name': url_name,
                                'transactions': transactions,
                                'month_filter': month_filter,
                                'year_filter': year_filter,
                                'monthDict': monthDict,
                                'income_category': income_category,
                                'incomeCategoriesDict': incomeCategoriesDict,
                                'expense_category': expense_category,
                                'expenseCategoriesDict' : expenseCategoriesDict})

            if request.POST.get('income_filter_history') is not None: # Если пользователь применил фильтр по категориям дохода
                if request.POST.get('income_filter_history').isdigit(): # Если значение фильтра по категориям дохода число
                    expense_category = None
                    income_category = int(request.POST.get('income_filter_history')) # Получение значения фильтра по категориям дохода
                    if income_category == 0:
                        transactions = utils.get_income_transaction_with_month_and_year_filter(year_filter, month_filter) # Получение всех транзакций дохода с учетом фильтра по месяцам и годам
                        
                        monthDict = utils.get_month() # Получение всех месяцев и годов существующих транзакций
                        incomeCategoriesDict = utils.get_income_categories() # Получение всех категорий дохода в существующих транзакциях
                        expenseCategoriesDict = utils.get_expense_categories() # Получение всех категорий расхода в существующих транзакциях

                        return render(
                                        request, 'core/history.html',
                                        {'url_name': url_name,
                                        'transactions': transactions,
                                        'month_filter': month_filter,
                                        'year_filter': year_filter,
                                        'monthDict': monthDict,
                                        'income_category': income_category,
                                        'incomeCategoriesDict': incomeCategoriesDict,
                                        'expense_category': expense_category,
                                        'expenseCategoriesDict' : expenseCategoriesDict})

                    if income_category != 0: # Если значение фильтра по категориям дохода любое число кроме нуля
                        transactions = utils.get_income_transaction_with_month_and_year_filter_and_category_filter(year_filter, month_filter, income_category) # Получение всех транзакций дохода с учетом фильтра по месяцам и годам и фильтра по категориям
                        monthDict = utils.get_month() # Получение всех месяцев и годов существующих транзакций
                        incomeCategoriesDict = utils.get_income_categories() # Получение всех категорий дохода в существующих транзакциях
                        expenseCategoriesDict = utils.get_expense_categories() # Получение всех категорий расхода в существующих транзакциях

                        return render(
                                        request, 'core/history.html',
                                        {'url_name': url_name,
                                        'transactions': transactions,
                                        'month_filter': month_filter,
                                        'year_filter': year_filter,
                                        'monthDict': monthDict,
                                        'income_category': income_category,
                                        'incomeCategoriesDict': incomeCategoriesDict,
                                        'expense_category': expense_category,
                                        'expenseCategoriesDict' : expenseCategoriesDict})

            if request.POST.get('expense_filter_history') == 'expense filter inner': # Если пользователь применил фильтр по категориям расхода
                income_category = None
                expense_category = request.POST.get('expense_filter_history') # Получение значения фильтра по категориям расхода

                transactions = utils.get_inner_transaction_with_month_and_year_filter(year_filter, month_filter) # Получение всех внутренних транзакций с учетом фильтра по месяцам и годам

                monthDict = utils.get_month() # Получение всех месяцев и годов существующих транзакций
                incomeCategoriesDict = utils.get_income_categories() # Получение всех категорий дохода в существующих транзакциях
                expenseCategoriesDict = utils.get_expense_categories() # Получение всех категорий расхода в существующих транзакциях

                return render(
                                request, 'core/history.html',
                                {'url_name': url_name,
                                'transactions': transactions,
                                'month_filter': month_filter,
                                'year_filter': year_filter,
                                'monthDict': monthDict,
                                'income_category': income_category,
                                'incomeCategoriesDict': incomeCategoriesDict,
                                'expense_category': expense_category,
                                'expenseCategoriesDict' : expenseCategoriesDict})

            if request.POST.get('expense_filter_history') is not None:
                if request.POST.get('expense_filter_history').isdigit():
                    income_category = None
                    expense_category = int(request.POST.get('expense_filter_history')) # Получение значения фильтра по категориям расхода

                    if expense_category == 0:
                        transactions = utils.get_expense_transaction_with_month_and_year_filter(year_filter, month_filter) # Получение всех транзакций расхода с учетом фильтра по месяцам и годам
                        monthDict = utils.get_month() # Получение всех месяцев и годов существующих транзакций
                        incomeCategoriesDict = utils.get_income_categories() # Получение всех категорий дохода в существующих транзакциях
                        expenseCategoriesDict = utils.get_expense_categories() # Получение всех категорий расхода в существующих транзакциях

                        return render(
                                        request, 'core/history.html',
                                        {'url_name': url_name,
                                        'transactions': transactions,
                                        'month_filter': month_filter,
                                        'year_filter': year_filter,
                                        'monthDict': monthDict,
                                        'income_category': income_category,
                                        'incomeCategoriesDict': incomeCategoriesDict,
                                        'expense_category': expense_category,
                                        'expenseCategoriesDict' : expenseCategoriesDict})

                    if expense_category != 0:
                            transactions = utils.get_expense_transaction_with_month_and_year_filter_and_category_filter(year_filter, month_filter, expense_category) # Получение всех транзакций расхода с учетом фильтра по месяцам и годам и фильтра по категориям
                            monthDict = utils.get_month() # Получение всех месяцев и годов существующих транзакций
                            incomeCategoriesDict = utils.get_income_categories() # Получение всех категорий дохода в существующих транзакциях
                            expenseCategoriesDict = utils.get_expense_categories() # Получение всех категорий расхода в существующих транзакциях

                            return render(
                                            request, 'core/history.html',
                                            {'url_name': url_name,
                                            'transactions': transactions,
                                            'month_filter': month_filter,
                                            'year_filter': year_filter,
                                            'monthDict': monthDict,
                                            'income_category': income_category,
                                            'incomeCategoriesDict': incomeCategoriesDict,
                                            'expense_category': expense_category,
                                            'expenseCategoriesDict' : expenseCategoriesDict})
    
    transactions = utils.get_all_transaction_with_month_and_year_filter(year_filter, month_filter) # Получение всех существующих транзакций с учетом фильтра по месяцам и годам
    monthDict = utils.get_month() # Получение всех месяцев и годов существующих транзакций
    incomeCategoriesDict = utils.get_income_categories() # Получение всех категорий дохода в существующих транзакциях
    expenseCategoriesDict = utils.get_expense_categories() # Получение всех категорий расхода в существующих транзакциях

    return render(
                    request, 'core/history.html',
                    {'url_name': url_name,
                    'transactions': transactions,
                    'month_filter': month_filter,
                    'year_filter': year_filter,
                    'monthDict': monthDict,
                    'income_category': income_category,
                    'incomeCategoriesDict': incomeCategoriesDict,
                    'expense_category': expense_category,
                    'expenseCategoriesDict' : expenseCategoriesDict})