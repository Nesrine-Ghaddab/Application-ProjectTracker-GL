from django.urls import path
from . import views

app_name = "Notes"

urlpatterns = [
	path('', views.index, name='index'),
	path('AddNote/', views.new_note, name='Add_Note'),
	path('DetailsNote/<int:note_id>/', views.details_note, name='Details_Note'),
	path('DetailsNote/EditNote/<int:note_id>/', views.edit_note, name='Edit_Note'),
	path('Details/Note/EditNote/<int:note_id>/Delete', views.delete_note, name='Delete_Note'),
	path('AddTag/', views.add_tag, name='Add_Tag')
]