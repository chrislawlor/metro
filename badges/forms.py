from django import forms

from .badges import PALLATES


PALLETE_CHOICES = [(p, p.upper()) for p in PALLATES]


class ButtonForm(forms.Form):
    subject = forms.CharField(max_length=30, required=False)
    text = forms.CharField(max_length=140)
    theme = forms.ChoiceField(choices=PALLETE_CHOICES)
