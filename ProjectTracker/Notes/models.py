from django.db import models

class Tag(models.Model):
	name = models.CharField(max_length=30, unique=True, null=False, blank=False)

	def __str__(self):
		return self.name

class Note(models.Model):
	title = models.CharField(max_length=60, blank=False, null=False)
	content = models.TextField(blank=True, null=True)
	tags = models.ManyToManyField(Tag, blank=True, related_name="notes")
	created_at = models.DateField(auto_now_add=True)
	update_at = models.DateField(auto_now=True)

	def __str__(self):
		return self.title