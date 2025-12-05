from django import forms
from .models import Project, Task
from django.utils import timezone

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'deadline', 'status']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline < timezone.now().date():
            raise forms.ValidationError("La date limite ne peut pas être dans le passé")
        return deadline

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'title', 'description', 'deadline', 'priority']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        """Initialize TaskForm.

        Accepts an optional `user` keyword argument. If provided, the
        `project` field queryset will be limited to that user's projects.
        If not provided, the queryset will be empty to avoid showing
        unrelated projects and to fail-fast in views that forgot to pass
        the user.
        """
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['project'].queryset = Project.objects.filter(user=user)
        else:
            # No user provided: keep queryset empty to avoid leaking other users' projects
            self.fields['project'].queryset = Project.objects.none()

class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'deadline', 'status', 'progress']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'progress': forms.NumberInput(attrs={'min': 0, 'max': 100, 'step': 1}),
        }
    
    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline < timezone.now().date():
            raise forms.ValidationError("La date limite ne peut pas être dans le passé")
        return deadline