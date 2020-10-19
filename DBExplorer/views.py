from django.views.generic.list import ListView

from core.models import Account, IncomeCategory, ExpenseCategory, IncomeTransaction, ExpenseTransaction, InnerTransaction


class AccountView(ListView):
    model = Account
    template_name = 'DBExplorer/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'Account'

        return context


class IncomeCategoryView(ListView):
    model = IncomeCategory
    template_name = 'DBExplorer/income_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'Income Category'

        return context


class ExpenseCategoryView(ListView):
    model = ExpenseCategory
    template_name = 'DBExplorer/expense_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'Expence Category'

        return context


class IncomeTransactionView(ListView):
    model = IncomeTransaction
    template_name = 'DBExplorer/income_transaction.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'Income Transaction'

        return context


class ExpenseTransactionView(ListView):
    model = ExpenseTransaction
    template_name = 'DBExplorer/expense_transaction.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'Expense Transaction'

        return context


class InnerTransactionView(ListView):
    model = InnerTransaction
    template_name = 'DBExplorer/inner_transaction.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'Inner Transaction'

        return context
