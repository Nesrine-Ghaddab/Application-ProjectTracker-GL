from django.urls import path
from . import views

app_name = "Notes"

urlpatterns = [
	path('', views.index, name='index'),
	path('AddNote/', views.new_note, name='Add_Note'),
	path('DetailsNote/<int:note_id>', views.details_note, name='Details_Note')
]