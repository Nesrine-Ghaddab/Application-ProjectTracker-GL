from django.shortcuts import render, redirect
from .models import Note, Tag
from .forms import NoteForm, TagForm, SearchTagForm

# Create your views here.
def index(request):
	tags = SearchTagForm()
	context = {"Notes" : Note.objects.all(), "tags" : tags}
	return render(request, "Notes/Notes.html", context)

def search_results(request):
	# Filter using the notes name
	search_input = request.GET.get("search_name")
	form_tag = SearchTagForm(request.GET)
	notes = Note.objects.all()
	tags = SearchTagForm()

	if search_input:
		notes = notes.filter(title__icontains=search_input)
	
	if form_tag.is_valid():
		search_tag = form_tag.cleaned_data.get('tags')
		if search_tag:
			notes = notes.filter(tags__name=search_tag)

	if notes == Note.objects.all():
		return redirect('Notes:index')
	return render(request, 'Notes/Notes.html', {'search_notes':notes, 'tags' : tags})


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

def details_tags(request):
	tags = Tag.objects.all()
	context = {"tags":tags}
	return render(request, "Notes/Details_Tags.html", context)

def add_tag(request):
    if request.method == "POST":
        tag_name = request.POST.get("new_tag")
        if tag_name:
            Tag.objects.create(name=tag_name)
        return redirect("Notes:Details_Tags")

def edit_tag(request, tag_id):
    tag = Tag.objects.get(pk=tag_id)
    if request.method == "POST":
        new_name = request.POST.get("name")
        if new_name:
            tag.name = new_name
            tag.save()
    return redirect("Notes:Details_Tags")


def delete_tag(request, tag_id):
	tag = Tag.objects.get(pk = tag_id)
	tag.delete()
	return redirect("Notes:Details_Tags")