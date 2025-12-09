from django.db import models
import markdown, bleach
from django.contrib.auth import get_user_model

User = get_user_model()

class Tag(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_tag_notes", default=1)
	name = models.CharField(max_length=30, unique=True, null=False, blank=False)

	def __str__(self):
		return self.name

class Note(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="user_notes", default=1)
	title = models.CharField(max_length=60, blank=False, null=False)
	content = models.TextField(blank=True, null=True)
	tags = models.ManyToManyField(Tag, blank=True, related_name="notes")
	created_at = models.DateField(auto_now_add=True)
	update_at = models.DateField(auto_now=True)

	def __str__(self):
		return self.title
	
	def content_html(self):
		raw_html = markdown.markdown(self.content, extensions=["fenced_code", "tables"])
		clean_html = bleach.clean(raw_html, tags=["p", "strong", "em", "blockquote", "b", "i", "ul", "li", "a", "code", "pre", "h1", "h2", "h3", "hr", "code"])
		return clean_html