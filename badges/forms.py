from django import forms

from .badges import PALLATES


PALLETE_CHOICES = [(p, p.upper()) for p in PALLATES]


class ButtonForm(forms.Form):
    text = forms.CharField(max_length=30)
    theme = forms.ChoiceField(choices=PALLETE_CHOICES)
