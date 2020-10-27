from django import forms
from core.models import Account, ExpenseCategory
from .CustomDateInput import CustomDateInput
from django.utils.translation import gettext as _
from core.utils import get_balance_d
from .CustomDateInput import CustomDateInput
from django.core.exceptions import ValidationError

from itertools import chain
from datetime import date

def get_account_choices():
    account_choices = []

    for account in Account.objects.all():
        account_choices.append(('acc__' + str(account.id), account.name))

    return account_choices


def get_category_choices():
    category_choices = []

    for category in ExpenseCategory.objects.all():
        category_choices.append(('cat__' + str(category.id), category.name))

    return category_choices



class ExpenceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
    amount_exp = forms.FloatField(min_value=0, label='Сумма', widget=forms.NumberInput(attrs = {
        'placeholder': 'Сумма'
    }))
    
    from_cat = forms.ChoiceField(
        label='В',
        choices=[(-1, "Откуда...")] + get_account_choices(),
        widget=forms.Select()
    )
    to_cat = forms.ChoiceField(
        label='Из',
        choices=[(-1, "Куда...")]+list(chain(get_category_choices(), get_account_choices())),
        widget=forms.Select()
    )
    when = forms.DateField(label='Дата', widget=CustomDateInput())
    commentary_exp = forms.CharField(label='Комментарий', required=False, widget=forms.Textarea(attrs = {
                'placeholder': 'Комментарий'
            }))

    
    def clean_when(self):
        date_when = self.cleaned_data['when']

        if date_when > date.today():
            raise ValidationError(_('Выберите корректную дату'), code='invalid')
        else:
            return date_when


    def clean(self):
        cleaned_data = super().clean()

        from_data = cleaned_data.get('from_cat')
        to_data = cleaned_data.get('to_cat')
        amount_data = cleaned_data.get('amount_exp')

        if from_data=="-1":
            raise ValidationError(_('Выберите откуда пришло'), code='invalid')
        if to_data=="-1":
            raise ValidationError(_('Выберите куда потратили'), code='invalid')
        
        # Было ли у нас нужное кол-во денег на тот период
        id = from_data.split('__')[1]
        balance = get_balance_d(id)

        if amount_data * 100 > balance:
            raise ValidationError(_('Недостаточно средств'), code='invalid')
        
        if from_data == to_data:
            # Пытаемся перевести деньги на то же месо хранения
            raise ValidationError(_('Выберите разные места хранения'), code='invalid')