from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from .CustomDateInput import CustomDateInput
from .utils import get_account_choices, get_income_category_choices

from itertools import chain
from datetime import date
from math import fabs


class IncomeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    amount = forms.FloatField(
        min_value=0,
        label='Сумма',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Сумма'
        })
    )

    from1 = forms.ChoiceField(
        label='Из',
        choices=[(-1, "Откуда...")] + list(chain(
            get_income_category_choices(),
            get_account_choices()
        ))
    )

    to = forms.ChoiceField(
        label='В',
        choices=[(-1, "Куда...")] + get_account_choices(),
        widget=forms.Select(attrs={
                'placeholder': 'Куда'
        })
    )

    date = forms.DateField(label='Дата', widget=CustomDateInput(attrs={
                'value': date.today()
    }))

    commentary = forms.CharField(
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
<<<<<<< HEAD
            raise ValidationError(_('Неверный формат суммы'), code='invalid')

        return data

    def clean_date(self):
        data = self.cleaned_data['date']

        if fabs(data.year - date.today().year) > 5:
            raise ValidationError(_('Неверный формат даты'), code='invalid')
=======
            self.fields['amount'].widget.attrs.update({'class': 'form-control is-invalid'})
            raise ValidationError(_('Неверный формат суммы'))
>>>>>>> main_page_new_design

        return data

    def clean_from1(self):
        data = self.cleaned_data['from1']

        if data == '-1':
            self.fields['from1'].widget.attrs.update({'class': 'form-control is-invalid'})
            raise ValidationError(_('Выберите откуда пришло'), code='invalid')

        return data

    def clean_to(self):
        data = self.cleaned_data['to']

        if data == '-1':
            self.fields['to'].widget.attrs.update({'class': 'form-control is-invalid'})
            raise ValidationError(_('Выберите куда начислить'), code='invalid')

        return data

    def clean(self):
        cleaned_data = super().clean()

        from_data = cleaned_data.get('from1')
        to_data = cleaned_data.get('to')

        if from_data == to_data:
            # Пытаемся перевести деньги на то же место хранения
            self.fields['from1'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.fields['to'].widget.attrs.update({'class': 'form-control is-invalid'})
            raise ValidationError(
                _('Выберите разные места хранения'),
                code='invalid'
            )
