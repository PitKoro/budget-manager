from django.shortcuts import render
from .models import Account


def test(request):
    url_name = request.resolver_match.url_name
    account_list = Account.objects.all()
    print(account_list[0].name)
    return render(request, 'core/test.html', {'account_list': account_list, 'url_name': url_name})

def report(request):
    url_name = request.resolver_match.url_name
    return render(request, 'core/report.html', {'url_name': url_name})

def history(request):
    url_name = request.resolver_match.url_name
    return render(request, 'core/history.html', {'url_name': url_name})