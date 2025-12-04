# PersonalTracker/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Reunion/', include('Reunion.urls')),  # Include Reunion app URLs at the root
     path('users/', include('UserApp.urls')),

    # keep API separate
    path('api/', include('Reunion.api_urls')),
]