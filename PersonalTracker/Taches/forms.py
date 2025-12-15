from django import forms
from .models import Taches


class TachesForm(forms.ModelForm):
    class Meta:
        model = Taches
        fields = ['titre', 'description', 'dateEcheance']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'dateEcheance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


