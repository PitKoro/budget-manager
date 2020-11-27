from django.urls import path

from . import views

urlpatterns = [
    path('account/', views.AccountView.as_view(), name='account'),
    path(
        'income-category/',
        views.IncomeCategoryView.as_view(),
        name='income-category'
    ),
    path(
        'expense-category/',
        views.ExpenseCategoryView.as_view(),
        name='expense-category'
    ),
    path(
        'income-transaction/',
        views.IncomeTransactionView.as_view(),
        name='income-transaction'
    ),
    path(
        'expense-transaction/',
        views.ExpenseTransactionView.as_view(),
        name='expence-transaction'
    ),
    path(
        'inner-transaction/',
        views.InnerTransactionView.as_view(),
        name='inner-transaction'
    )
]
