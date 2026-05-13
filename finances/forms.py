from django import forms

from .models import Table, Transaction


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ("name", "description", "color")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "color": forms.TextInput(attrs={"type": "color", "class": "form-control form-control-color"}),
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ("title", "amount", "currency", "date", "categories")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "currency": forms.Select(attrs={"class": "form-select"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "categories": forms.CheckboxSelectMultiple(),
        }