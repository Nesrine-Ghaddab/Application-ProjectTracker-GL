from django.urls import path
from . import views

app_name = "Notes"

urlpatterns = [
	path('', views.index, name='index'),
	path('AddNote/', views.new_note, name='Add_Note'),
	path('DetailsNote/<int:note_id>/', views.details_note, name='Details_Note'),
	path('DetailsNote/EditNote/<int:note_id>/', views.edit_note, name='Edit_Note'),
	path('Details/Note/EditNote/<int:note_id>/Delete', views.delete_note, name='Delete_Note'),
	path('DetailsTags/', views.details_tags, name='Details_Tags'),
	path('DetailsTags/AddTag/', views.add_tag, name='Add_Tag'),
	path('DetailsTags/EditTag/<int:tag_id>/', views.edit_tag, name='Edit_Tag'),
	path('DetailsTags/DeleteTag/<int:tag_id>/', views.delete_tag, name='Delete_Tag'),
	path('Search/', views.search_results, name='search_results')
]