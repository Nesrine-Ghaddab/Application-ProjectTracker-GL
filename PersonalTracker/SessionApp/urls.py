from django.urls import path
from . import views

app_name = "study"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("app/", views.home, name="home"),

    # API
    path("api/sessions/start/", views.api_session_start, name="api_session_start"),
    path("api/sessions/stop/", views.api_session_stop, name="api_session_stop"),
    path("api/sessions/recent/", views.api_recent_sessions, name="api_recent_sessions"),
    path("api/summary/", views.api_summary, name="api_summary"),

    # Historique (Voir tout)
    path("history/", views.session_list, name="session_list"),

    # CRUD
    path("history/new/", views.session_create, name="session_create"),
    path("history/<int:pk>/edit/", views.session_update, name="session_update"),
    path("history/<int:pk>/delete/", views.session_delete, name="session_delete"),
    path("sessions/<int:pk>/pdf/", views.session_pdf, name="session_pdf"),

    # 🔵 Nouveau : renommage AJAX
    path(
        "history/<int:pk>/rename/",
        views.session_rename,
        name="session_rename",
    ),
]
