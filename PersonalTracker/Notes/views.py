from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Note, Tag
from .forms import NoteForm, TagForm, SearchTagForm

#  =========== NOTES ===========

@login_required
def index(request):
	tags = SearchTagForm(user = request.user)
	context = {"Notes" : Note.objects.filter(user=request.user), "tags" : tags}
	return render(request, "Notes/Notes.html", context)

@login_required
def search_results(request):
	# Filter using the notes name
	search_input = request.GET.get("search_name")
	form_tag = SearchTagForm(request.GET, user = request.user)
	notes = Note.objects.filter(user=request.user)
	tags = SearchTagForm(user = request.user)

	if search_input:
		notes = notes.filter(title__icontains=search_input)
	
	if form_tag.is_valid():
		search_tag = form_tag.cleaned_data.get('tags')
		if search_tag:
			notes = notes.filter(tags__name=search_tag)

	if notes == Note.objects.filter(user=request.user):
		return redirect('Notes:index')
	return render(request, 'Notes/Notes.html', {'search_notes':notes, 'tags' : tags})

@login_required
def new_note(request):
	if request.method == 'POST':
		form = NoteForm(request.POST, user=request.user)

		if (form.is_valid()):
			note = form.save(commit=False)
			note.user = user=request.user
			note.save()
			form.save_m2m()
			return redirect('Notes:index')
	else:
		form = NoteForm(user=request.user)
	return render(request, "Notes/Add_Note.html", {"form": form})

@login_required
def details_note(request, note_id):
	note_content = Note.objects.get(pk = note_id, user=request.user)
	return render(request, "Notes/Details_Note.html", {"note":note_content})

@login_required
def edit_note(request, note_id):
	note = Note.objects.get(pk = note_id, user=request.user)
	if request.method == 'POST':
		form = NoteForm(request.POST, instance=note, user=request.user)

		if (form.is_valid()):
			form.save()
			return redirect('Notes:Details_Note', note_id=note.id)
	else:
		form = NoteForm(instance=note, user=request.user)
	return render(request, "Notes/Edit_Note.html", {"note_object": note, "note":form, "note_id": note_id, "date_update": note.update_at})

@login_required
def delete_note(request, note_id):
	note = Note.objects.get(pk = note_id, user=request.user)
	note.delete()
	return redirect('Notes:index')

#  =========== TAGS ===========

@login_required
def details_tags(request):
	tags = Tag.objects.filter(user=request.user)
	context = {"tags":tags}
	return render(request, "Notes/Details_Tags.html", context)

@login_required
def add_tag(request):
    if request.method == "POST":
        tag_name = request.POST.get("new_tag")
        if tag_name:
            Tag.objects.create(name=tag_name, user=request.user)
        return redirect("Notes:Details_Tags")

@login_required
def edit_tag(request, tag_id):
    tag = Tag.objects.get(pk=tag_id)
    if request.method == "POST":
        new_name = request.POST.get("name")
        if new_name:
            tag.name = new_name
            tag.save()
    return redirect("Notes:Details_Tags")


@login_required
def delete_tag(request, tag_id):
	tag = Tag.objects.get(pk = tag_id)
	tag.delete()
	return redirect("Notes:Details_Tags")

@login_required
def clear_unused_tags(request):
	tags = Tag.objects.filter(user=request.user)
	notes = Note.objects.filter(user=request.user)

	for tag in tags:
		if not(Note.objects.filter(user=request.user, tags__name=tag)):
			tag.delete()
	return redirect("Notes:Details_Tags")