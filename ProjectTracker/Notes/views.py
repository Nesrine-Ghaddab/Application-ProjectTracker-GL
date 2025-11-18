from django.shortcuts import render, redirect
from .models import Note, Tag
from .forms import NoteForm

# Create your views here.
def index(request):
	context = {"Notes" : Note.objects.all()}
	return render(request, "Notes/Notes.html", context)

def new_note(request):
	if request.method == 'POST':
		form = NoteForm(request.POST)

		if (form.is_valid()):
			form.save()
			return redirect('Notes:index')
	else:
		form = NoteForm()
	return render(request, "Notes/Add_Note.html", {"form": form})

def details_note(request, note_id):
	note_content = Note.objects.get(pk = note_id)
	return render(request, "Notes/Details_Note.html", {"note":note_content})