from django.shortcuts import render, redirect
from .models import Note, Tag
from .forms import NoteForm, TagForm

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

def edit_note(request, note_id):
	note = Note.objects.get(pk = note_id)
	if request.method == 'POST':
		form = NoteForm(request.POST, instance=note)

		if (form.is_valid()):
			form.save()
			return redirect('Notes:Details_Note', note_id=note.id)
	else:
		form = NoteForm(instance=note)
	return render(request, "Notes/Edit_Note.html", {"note_object": note, "note":form, "note_id": note_id, "date_update": note.update_at})

def delete_note(request, note_id):
	note = Note.objects.get(pk = note_id)
	note.delete()
	return redirect('Notes:index')

def add_tag(request):
    if request.method == "POST":
        tag_name = request.POST.get("new_tag")
        if tag_name:
            Tag.objects.create(name=tag_name)
        return redirect("Notes:index")
