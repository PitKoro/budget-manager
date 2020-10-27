from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from core.models import Account, IncomeCategory
from core.utils import get_balance
from .CustomDateInput import CustomDateInput
from .utils import get_account_choices, get_category_choices

from itertools import chain
from datetime import date





class IncomeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    amount = forms.FloatField(min_value=0, label='Сумма', widget=forms.NumberInput(attrs = {
        'placeholder': 'Сумма'
    }))
    from1 = forms.ChoiceField(
        label='Из',
        choices=[(-1, "Откуда...")]+list(chain(get_category_choices(), get_account_choices()))
    )
    to = forms.ChoiceField(
        label='В',
        choices=[(-1, "Куда...")] + get_account_choices(),
        widget=forms.Select(attrs = {
                'placeholder': 'Куда'
            })
    )
    date = forms.DateField(label='Дата', widget=CustomDateInput())
    commentary = forms.CharField(label='Комментарий', required=False, widget=forms.Textarea(attrs = {
                'placeholder': 'Комментарий'
            }))

    def clean_amount(self):
        data = self.cleaned_data['amount']
        decimal_part = str(data*100).split('.')[1]

        if len(decimal_part) > 1 or int(decimal_part) != 0:
            raise ValidationError(_('Неверный формат суммы'))
        else:
            return data

    def clean_date(self):
        data = self.cleaned_data['date']

        if data > date.today():
            raise ValidationError(_('Неверный формат даты'))
        else:
            return data

    def clean(self):
        cleaned_data = super().clean()

        from_data = cleaned_data.get('from1')
        to_data = cleaned_data.get('to')
        amount_data = cleaned_data.get('amount')

        if from_data=="-1":
            raise ValidationError(_('Выберите откуда пришло'), code='invalid')
        if to_data=="-1":
            raise ValidationError(_('Выберите куда начислить'), code='invalid')

        
        if from_data == to_data:
            # Пытаемся перевести деньги на то же месо хранения
            raise ValidationError(_('Выберите разные места хранения'), code='invalid')

        if from_data.startswith('acc__'):
            # Перевод денег с одного места хранения на другое
            id = from_data.split('__')[1]
            balance = get_balance(Account.objects.get(id=id))

            if amount_data * 100 > balance:
                raise ValidationError(_('Недостаточно средств'), code='invalid')
    