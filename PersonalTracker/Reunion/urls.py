# Reunion/urls.py
from django.urls import path
from . import views

# Application namespace for reversing (used as 'reunion:...')
app_name = 'reunion'

urlpatterns = [
    path('', views.ReunionList.as_view(), name='list'),
    path('reunion/<int:pk>/', views.ReunionDetail.as_view(), name='detail'),
    path('reunion/create/', views.ReunionCreate.as_view(), name='create'),
    path('reunion/<int:pk>/update/', views.ReunionUpdate.as_view(), name='update'),
    path('reunion/<int:pk>/delete/', views.ReunionDelete.as_view(), name='delete'),

    path('reminders/', views.ReminderLogList.as_view(), name='reminder_list'),
    path('reminders/<int:pk>/', views.ReminderLogDetail.as_view(), name='reminder_detail'),
    path('reminders/<int:pk>/delete/', views.ReminderLogDelete.as_view(), name='reminder_delete'),
]