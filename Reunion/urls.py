# Reunion/urls.py
from django.urls import path
from . import views
from django.urls import include

# No app_name needed (no namespace)
urlpatterns = [
    path('', views.ReunionList.as_view(), name='reunion_list'),  # Home page shows meetings
    path('reunion/<int:pk>/', views.ReunionDetail.as_view(), name='reunion_detail'),
    path('reunion/create/', views.ReunionCreate.as_view(), name='reunion_create'),
    path('reunion/<int:pk>/update/', views.ReunionUpdate.as_view(), name='reunion_update'),
    path('reunion/<int:pk>/delete/', views.ReunionDelete.as_view(), name='reunion_delete'),
    
    path('reminders/', views.ReminderLogList.as_view(), name='reminderlog_list'),
    path('reminders/<int:pk>/', views.ReminderLogDetail.as_view(), name='reminderlog_detail'),
    path('reminders/<int:pk>/delete/', views.ReminderLogDelete.as_view(), name='reminderlog_delete'),
]