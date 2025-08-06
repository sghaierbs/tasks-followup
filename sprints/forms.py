from django import forms
from .models import Sprint

class SprintForm(forms.ModelForm):
    class Meta:
        model = Sprint
        fields = ['name', 'planned_start_date', 'planned_end_date', 'is_current']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sprint name'}),
            'planned_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'planned_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        labels = {
            'is_current': 'Is current sprint'
        }