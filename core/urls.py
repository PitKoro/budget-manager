from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('report', views.report, name='report'),
    path('history', views.history, name='history')
]
