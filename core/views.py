from django.shortcuts import render
from itertools import chain
from operator import attrgetter
from .models import Account, IncomeTransaction, ExpenseTransaction, InnerTransaction


def main(request):
    url_name = request.resolver_match.url_name
    account_list = Account.objects.all()
    return render(request, 'core/main.html', {'account_list': account_list, 'url_name': url_name})

def report(request):
    url_name = request.resolver_match.url_name
    return render(request, 'core/report.html', {'url_name': url_name})

def history(request):
    url_name = request.resolver_match.url_name
    incomeT = IncomeTransaction.objects.all()
    expenseT = ExpenseTransaction.objects.all()
    innerT = InnerTransaction.objects.all()
    transactions = sorted((chain(incomeT, expenseT, innerT)), key=attrgetter('date'), reverse=True)   
    return render(request, 'core/history.html', {'url_name': url_name, 'transactions':transactions})