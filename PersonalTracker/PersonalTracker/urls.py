from django.contrib import admin
from django.urls import path, include
from SessionApp import views as session_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", session_views.landing, name="home"),

    path("sessions/", include("SessionApp.urls")),

    path("accounts/", include("UserApp.urls")),
    path("accounts/", include("django.contrib.auth.urls")),

    path("captcha/", include("captcha.urls")),

    path("projects/", include(("Gestion_Projects.urls", "projects"), namespace="projects")),

    path("Reunion/", include(("Reunion.urls", "reunion"), namespace="reunion")),
	path('Notes/', include('Notes.urls')),
]

# SERVE MEDIA FILES (IMPORTANT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)