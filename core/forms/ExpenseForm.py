from django import forms
from core.models import Account
from .CustomDateInput import CustomDateInput
from django.utils.translation import gettext as _
from core.utils import get_balance
from django.core.exceptions import ValidationError
from .utils import get_account_choices, get_expense_category_choices

from itertools import chain
from datetime import date


class ExpenseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    amount_exp = forms.FloatField(
        min_value=0,
        label='Сумма',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Сумма'
        })
    )

    from_cat = forms.ChoiceField(
        label='В',
        choices=[(-1, "Откуда...")] + get_account_choices(),
        widget=forms.Select()
    )

    to_cat = forms.ChoiceField(
        label='Из',
        choices=[(-1, "Куда...")] + list(chain(
            get_expense_category_choices(),
            get_account_choices()
        )),
        widget=forms.Select()
    )

    when = forms.DateField(label='Дата', widget=CustomDateInput(attrs={
                'value': date.today()
    }))

    commentary_exp = forms.CharField(
        label='Комментарий',
        required=False,
        widget=forms.Textarea(attrs={
                'placeholder': 'Комментарий'
        })
    )

    def clean_amount(self):
        data = self.cleaned_data['amount']
        decimal_part = str(data*100).split('.')[1]

        if len(decimal_part) > 1 or int(decimal_part) != 0:
            self.fields['amount'].widget.attrs.update({'class': 'form-control is-invalid'})
            raise ValidationError(_('Неверный формат суммы'))

        return data

    def clean_from_cat(self):
        data = self.cleaned_data['from_cat']

        if data == '-1':
            self.fields['from_cat'].widget.attrs.update({'class': 'form-control is-invalid'})
            raise ValidationError(
                _('Выберите откуда'),
                code='invalid'
            )

        return data

    def clean_to_cat(self):
        data = self.cleaned_data['to_cat']

        if data == '-1':
            self.fields['to_cat'].widget.attrs.update({'class': 'form-control is-invalid'})
            raise ValidationError(_('Выберите куда потрачено'), code='invalid')

        return data

    def clean(self):
        cleaned_data = super().clean()

        from_data = cleaned_data.get('from_cat')
        to_data = cleaned_data.get('to_cat')

        if from_data == to_data:
            # Пытаемся перевести деньги на то же место хранения
            self.fields['from_cat'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.fields['to_cat'].widget.attrs.update({'class': 'form-control is-invalid'})
            raise ValidationError(
                _('Выберите разные места хранения'),
                code='invalid'
            )
