from django.contrib import admin
from django.urls import path, include
from SessionApp import views as session_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # page d’accueil -> ton index base_tailwind
    path("", session_views.landing, name="home"),

    # tout ce qui concerne le timer / CRUD des sessions
    path("sessions/", include("SessionApp.urls")),

    # URLs d’auth Django (login, logout, password reset…)
    path("accounts/", include("django.contrib.auth.urls")),
]
