from django.shortcuts import render
from .models import Note, Tag

# Create your views here.
def index(request):
	context = {"Notes" : Note.objects.all()}
	return render(request, "Notes/Notes.html", context)