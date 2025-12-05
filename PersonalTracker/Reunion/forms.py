from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Reunion


class ReunionForm(forms.ModelForm):
    """Custom form for Reunion with enhanced validation"""
    
    class Meta:
        model = Reunion
        fields = [
            'title', 'date', 'start_time', 'end_time', 'reunion_type', 
            'subject', 'description', 'reminder_enabled', 'reminder_timing'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Meeting title'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'min': timezone.now().date()}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'reunion_type': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'reminder_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'reminder_timing': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Meeting Title',
            'date': 'Meeting Date',
            'start_time': 'Start Time',
            'end_time': 'End Time',
            'reunion_type': 'Type of Reunion',
            'subject': 'Subject',
            'description': 'Description (Optional)',
            'reminder_enabled': 'Enable Email Reminder',
            'reminder_timing': 'Reminder Timing',
        }
    
    def clean_date(self):
        """Validate that date is not in the past"""
        date = self.cleaned_data.get('date')
        if date and date < timezone.now().date():
            raise ValidationError("The meeting date cannot be in the past.")
        return date
    
    def clean(self):
        """Validate the entire form"""
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        errors = {}
        
        # Check if it's today and start time is in the past
        if date == timezone.now().date() and start_time:
            if start_time < timezone.now().time():
                errors['start_time'] = 'The meeting start time cannot be in the past.'
        
        # Check if start time is after or equal to end time
        if start_time and end_time:
            if start_time >= end_time:
                errors['end_time'] = 'The end time must be after the start time.'
        
        if errors:
            raise ValidationError(errors)
        
        return cleaned_data
