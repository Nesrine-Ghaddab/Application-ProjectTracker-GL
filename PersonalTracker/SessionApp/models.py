from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="study_sessions")
    title = models.CharField(max_length=120, blank=True)
    planned_minutes = models.PositiveIntegerField(default=50)
    break_minutes = models.PositiveIntegerField(default=10)

    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    is_running = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # NEW

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.title or 'Session'} ({self.user})"

    def stop(self):
        """Arrête une session en cours et calcule la durée."""
        if not self.is_running:
            return
        self.ended_at = timezone.now()
        self.duration_seconds = max(0, int((self.ended_at - self.started_at).total_seconds()))
        self.is_running = False

    def recalc_duration_if_possible(self):
        """Recalcule la durée si dates connues et session non en cours."""
        if self.started_at and self.ended_at and not self.is_running:
            self.duration_seconds = max(0, int((self.ended_at - self.started_at).total_seconds()))

    @property
    def duration_minutes(self):
        return round(self.duration_seconds / 60, 1)

    @staticmethod
    def streak_for_user(user: User) -> int:
        if not user.is_authenticated:
            return 0
        qs = (StudySession.objects
              .filter(user=user)
              .values_list(models.functions.TruncDate("started_at"), flat=True)
              .distinct())
        days = set(qs)
        if not days:
            return 0
        today = timezone.localdate()
        streak = 0
        cur = today
        while cur in days:
            streak += 1
            cur -= timedelta(days=1)
        return streak

    @staticmethod
    def suggest_duration_for_user(user: User, default=50) -> int:
        qs = (StudySession.objects
              .filter(user=user, is_running=False)
              .order_by("-started_at")[:5])
        last = list(qs)
        if len(last) >= 2 and all(s.duration_seconds < 45*60 for s in last[:2]):
            return 40
        if last:
            avg = sum(s.duration_seconds for s in last)/len(last)/60
            if avg >= 55:
                return 60
        return default
