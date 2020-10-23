from django import forms


from datetime import date



class ExpenceForm(forms.Form):
    amount = forms.FloatField()
    to_cat = forms.ChoiceField()
    from_cat = forms.ChoiceField()
    when = forms.DateTimeField()
    commentary = forms.CharField(widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    