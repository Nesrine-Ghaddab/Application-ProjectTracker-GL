# Reunion/api_urls.py
from django.urls import path
from . import api_views

urlpatterns = [
    path("api/reunions/", api_views.ReunionListAPI.as_view(), name="api_reunion_list"),
    path("api/reunion/", api_views.ReunionDetailAPI.as_view(), name="api_reunion_create"),  # POST to create
    path("api/reunion/<int:pk>/", api_views.ReunionDetailAPI.as_view(), name="api_reunion_detail"),
    path("api/reminder-logs/", api_views.ReminderLogListAPI.as_view(), name="api_reminder_logs"),
]
