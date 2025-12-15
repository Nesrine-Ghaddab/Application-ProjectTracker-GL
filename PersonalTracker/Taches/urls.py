from django.urls import path
from . import views

app_name = "Taches"




urlpatterns = [
    path('projet/taches/', views.FrontOfficeView.as_view(), name='frontoffice'),
    path('projet/<int:projet_id>/taches/', views.ProjectTachesListView.as_view(), name='project_taches'),
    path('projet/<int:projet_id>/priorisation/', views.PriorisationView.as_view(), name='priorisation'),

    #path('', views.FrontOfficeView.as_view(), name='frontoffice'),
    #path('priorisation/', views.PriorisationView.as_view(), name='priorisation'),
    path('tache/<int:pk>/terminer/', views.terminer_tache, name='tache_terminer'),
    path('tache/<int:pk>/', views.TachesDetailView.as_view(), name='tache_detail'),
    #path('tache/create/', views.TachesCreateView.as_view(), name='tache_create'),
    path('projet/<int:projet_id>/ajouter-tache/', views.TachesCreateView.as_view(), name='tache_create'),
    path('tache/<int:pk>/update/', views.TachesUpdateView.as_view(), name='tache_update'),
    path('tache/<int:pk>/delete/', views.TachesDeleteView.as_view(), name='tache_delete'),
]

