from django.contrib import admin
from .models import StudySession

@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "is_running", "started_at", "ended_at", "duration_minutes")
    list_filter = ("is_running",)
    search_fields = ("user__username", "title")
