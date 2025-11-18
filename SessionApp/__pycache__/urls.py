from django.urls import path
from . import views

app_name = "sessions"

urlpatterns = [
    path("", views.session_list, name="list"),              # /sessions/
    path("new/", views.session_create, name="create"),      # /sessions/new/
    path("<int:pk>/edit/", views.session_update, name="update"),   # /sessions/1/edit/
    path("<int:pk>/delete/", views.session_delete, name="delete"), # /sessions/1/delete/
]
