from django import forms
from .models import Note, Tag

class NoteForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), label="Tags", required=False)
    class Meta:
        model = Note
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full rounded-lg bg-slate-100 dark:bg-slate-800 px-3 py-2 outline-none focus:ring-2 ring-brand-600',
                'placeholder': 'Titre…'
            }),
            'content': forms.Textarea(attrs={
                'rows': 6,
                'class': 'w-full rounded-lg bg-slate-100 dark:bg-slate-800 px-3 py-2 outline-none focus:ring-2 ring-brand-600',
                'placeholder': 'Écris ta note…'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'w-full border border-slate-300 rounded-xl px-3 py-2 focus:outline-none focus:ring-2 focus:ring-slate-400'
            })
        }

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

class SearchTagForm(forms.ModelForm):
    tags = forms.ModelChoiceField(queryset=Tag.objects.all(), label = False)

    class Meta:
        model = Tag
        fields = ['tags']
        widgets = {
            'tags': forms.Select(attrs={
                'class': 'w-full border border-slate-300 rounded-xl px-3 py-2 focus:outline-none focus:ring-2 focus:ring-slate-400',
                'style': 'width: 200px; height: 35px; border-radius: 20px; font-size: 14px; padding: 0 10px; border: 1px solid #ccc; display: inline-flex; align-items: center; color: black; margin-top: 10px;'
            })
        }