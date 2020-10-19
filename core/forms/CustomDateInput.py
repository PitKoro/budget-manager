from django import forms


class CustomDateInput(forms.DateInput):
    input_type = 'date'
