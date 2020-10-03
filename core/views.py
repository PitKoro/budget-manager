from django.shortcuts import render
from .models import Account


def test(request):
    account_list = Account.objects.all()
    print(account_list[0].name)
    return render(request, 'core/test.html', {'account_list': account_list})
