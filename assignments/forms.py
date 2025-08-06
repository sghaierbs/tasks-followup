# assignments/forms.py
from django import forms
from .models import Assignment

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        exclude = ['created_by', 'created_at']
        fields = ['planned_start_date', 'planned_end_date', 'start_date', 'end_date', 'assignment_type', 'status', 'assignee', 'completion']
        widgets = {
            'planned_start_date': forms.DateInput(attrs={'type': 'date','class': 'form-select'}),
            'planned_end_date': forms.DateInput(attrs={'type': 'date','class': 'form-select'}),
            'assignment_type': forms.Select(attrs={'class': 'form-select'}),
            'assignee': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'type': 'date','class': 'form-select'}),
            'end_date': forms.DateInput(attrs={'type': 'date','class': 'form-select'}),
            'completion': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100, 'step': 1, 'placeholder': 'Enter percentage'}),
        }
        
        labels = {
            'planned_start_date': 'Start date',
            'planned_end_date': 'End date',
            'start_date': 'Actual start date',
            'end_date': 'Actual end date',
            'completion': 'Completion (%)',
        }