from django import forms
from django.utils import timezone
from .models import StudySession

class StudySessionForm(forms.ModelForm):
    class Meta:
        model = StudySession
        fields = ["title", "planned_minutes", "break_minutes", "started_at", "ended_at"]
        widgets = {
            "started_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "ended_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get("started_at")
        end = cleaned.get("ended_at")
        if end and start and end < start:
            raise forms.ValidationError("La date de fin doit être après la date de début.")
        return cleaned

    def save(self, user, instance: StudySession | None = None, commit=True):
        obj = instance or StudySession(user=user)
        for f in ["title","planned_minutes","break_minutes","started_at","ended_at"]:
            setattr(obj, f, self.cleaned_data.get(f))
        # si ended_at existe, la session n'est pas en cours
        obj.is_running = not bool(obj.ended_at)
        obj.recalc_duration_if_possible()
        if commit:
            obj.save()
        return obj
