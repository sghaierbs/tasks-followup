# tasks/forms.py
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'is_completed', 'status', 'classification', 'urgency', 'completed_at', 'assignee', 'visibility']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':16}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'classification': forms.Select(attrs={'class': 'form-select'}),
            'urgency': forms.Select(attrs={'class': 'form-select'}),
            'assignee': forms.Select(attrs={'class': 'form-select'}),
            #'created_by': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'type': 'date','class': 'form-select'}),
            'completed_at': forms.DateInput(attrs={'type': 'date','class': 'form-select','readonly': 'readonly'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'visibility': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # If editing and the user is not the creator, disable or hide the field
        if self.instance.pk and self.instance.created_by != self.user:
            self.fields['visibility'].disabled = True  # Makes it read-only
    
