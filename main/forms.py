from django import forms
from django.forms import ModelForm
from .models import Dataset

class DatasetForm(ModelForm):
    current_columns = forms.IntegerField(widget=forms.HiddenInput(), min_value=1, required=False)

    class Meta:
        model = Dataset
        fields = ['title', 'num_rows']
        widgets = {
            "title": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название датасета',
                'style': ' width: 41%;display: inline-block; margin-left: 60px;',

        }),
            "num_rows": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Количество строк',
                'style': 'width: 41%; display: inline-block;'
            }),
        }
