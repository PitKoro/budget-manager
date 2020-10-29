from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('', views.main, name='main'),
    path('report', views.report, name='report'),
    path('history', views.history, name='history')
]
