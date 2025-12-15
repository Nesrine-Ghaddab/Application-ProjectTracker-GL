from django.utils import timezone
from django.conf import settings  
from datetime import date
from django.db import models
from django.utils import timezone

class Project(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Non commencé'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminé'),
        ('on_hold', 'En pause'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    deadline = models.DateField(verbose_name="Date limite")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='not_started'
    )
    progress = models.FloatField(default=0.0, verbose_name="Progression (%)")
    total_time = models.FloatField(default=0.0, verbose_name="Temps total (heures)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
    
    def __str__(self):
        return self.title
    
    @property
    def is_overdue(self):
        return self.deadline < timezone.now().date() and self.status != 'completed'
    @property
    def is_overdue(self):
        return date.today() > self.deadline
    
    @property
    def days_remaining(self):
        today = timezone.now().date()
        return (self.deadline - today).days

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Basse'),
        ('medium', 'Moyenne'),
        ('high', 'Haute'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    deadline = models.DateField(verbose_name="Date limite")
    priority = models.CharField(
        max_length=10, 
        choices=PRIORITY_CHOICES, 
        default='medium'
    )
    is_completed = models.BooleanField(default=False, verbose_name="Terminée")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['deadline', 'priority']
        verbose_name = "Tâche"
        verbose_name_plural = "Tâches"
    
    def __str__(self):
        return self.title
    
    
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.message[:30]}"