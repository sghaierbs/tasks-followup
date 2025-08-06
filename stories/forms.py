from django import forms
from .models import UserStory


class UserStoryForm(forms.ModelForm):
    
    class Meta:
        model = UserStory
        fields = ['title', 'description', 'planned_start_date', 'planned_end_date', 'assignee', 'sprint', 'status', 'urgency']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'dir':'auto'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'dir':'auto', 'rows':'15'}),
            'assignee': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'urgency': forms.Select(attrs={'class': 'form-select'}),
            'sprint': forms.HiddenInput(),
            'planned_start_date': forms.DateInput(attrs={'type': 'date','class': 'form-select'}),
            'planned_end_date': forms.DateInput(attrs={'type': 'date','class': 'form-select'}),
            
        }
        labels = {
            'planned_start_date': 'Start date',
            'planned_end_date': 'End date',
        }


class UserStoryUpdateForm(forms.ModelForm):
    
    class Meta:
        model = UserStory
        fields = ['title', 'description', 'planned_start_date', 'planned_end_date', 'assignee', 'sprint', 'status', 'urgency', 'start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'dir':'auto'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'dir':'auto', 'rows':'15'}),
            'assignee': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'urgency': forms.Select(attrs={'class': 'form-select'}),
            'sprint': forms.HiddenInput(),
            'planned_start_date': forms.DateInput(attrs={'type': 'date','class': 'form-select'}),
            'planned_end_date': forms.DateInput(attrs={'type': 'date','class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'type': 'date','class': 'form-select'}),
            'end_date': forms.DateInput(attrs={'type': 'date','class': 'form-select'}),
            
        }
        labels = {
            'planned_start_date': 'Start date',
            'planned_end_date': 'End date',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields read-only (disabled in form)
        readonly_fields = ['planned_start_date', 'planned_end_date', 'assignee', 'status', 'start_date', 'end_date']
        for field in readonly_fields:
            self.fields[field].disabled = True