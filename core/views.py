from django.shortcuts import render
from .forms.IncomeForm import IncomeForm
from .models import Account
from .utils import get_balance, post_income_transaction


def main(request):
    # Обработка формы
    if request.method == 'POST':
        form = IncomeForm(request.POST)

        if form.is_valid():
            post_income_transaction(form.cleaned_data)
    else:
        form = IncomeForm()

    url_name = request.resolver_match.url_name
    account_list = []

    for account in Account.objects.all():
        # TODO: Всегда оставлять два знака после запятой в сумме
        account_list.append({
            'name': account.name,
            'amount': get_balance(account)/100
        })

    return render(request, 'core/main.html', {
        'account_list': account_list,
        'url_name': url_name,
        'income_form': form
    })


def report(request):
    url_name = request.resolver_match.url_name
    return render(request, 'core/report.html', {'url_name': url_name})


def history(request):
    url_name = request.resolver_match.url_name
    return render(request, 'core/history.html', {'url_name': url_name})
