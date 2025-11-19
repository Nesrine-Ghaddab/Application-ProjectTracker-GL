from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from datetime import datetime, timedelta

class Reunion(models.Model):
    # Reunion type choices
    REUNION_TYPES = [
        ('education', 'Education Course'),
        ('project', 'Project Meeting'),
        ('revision', 'Revision with Classmates'),
        ('other', 'Other'),
    ]
    
    # Subject choices
    SUBJECT_CHOICES = [
        ('math', 'Mathematics'),
        ('physics', 'Physics'),
        ('computer_science', 'Computer Science'),
        ('biology', 'Biology'),
        ('chemistry', 'Chemistry'),
        ('literature', 'Literature'),
        ('history', 'History'),
        ('other', 'Other'),
    ]
    
    # Reminder timing choices (in minutes before meeting)
    REMINDER_CHOICES = [
        (5, '5 minutes before'),
        (15, '15 minutes before'),
        (30, '30 minutes before'),
        (60, '1 hour before'),
        (120, '2 hours before'),
        (1440, '1 day before'),
        (2880, '2 days before'),
    ]
    
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    reunion_type = models.CharField(max_length=20, choices=REUNION_TYPES)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    title = models.CharField(max_length=200, help_text="Brief title for the meeting")
    description = models.TextField(blank=True, help_text="Additional details about the meeting")
    
    # Reminder fields
    reminder_enabled = models.BooleanField(default=True, help_text="Enable reminders for this meeting")
    reminder_timing = models.IntegerField(
        choices=REMINDER_CHOICES, 
        default=30,
        help_text="When to send reminder before the meeting"
    )
    reminder_sent = models.BooleanField(default=False, help_text="Whether reminder has been sent")
    reminder_sent_at = models.DateTimeField(null=True, blank=True, help_text="When the reminder was sent")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.date} ({self.get_reunion_type_display()})"
    
    @property
    def datetime(self):
        """Combine date and time for easier datetime operations"""
        return timezone.make_aware(
            datetime.combine(self.date, self.start_time)
        )
    
    @property
    def reminder_datetime(self):
        """Calculate when the reminder should be sent"""
        if not self.reminder_enabled:
            return None
        meeting_datetime = self.datetime
        reminder_minutes = self.reminder_timing
        return meeting_datetime - timedelta(minutes=reminder_minutes)
    
    @property
    def is_upcoming(self):
        """Check if meeting is in the future"""
        return self.datetime > timezone.now()
    
    @property
    def needs_reminder(self):
        """Check if reminder needs to be sent"""
        if not self.reminder_enabled or self.reminder_sent or not self.is_upcoming:
            return False
        
        reminder_time = self.reminder_datetime
        if reminder_time and reminder_time <= timezone.now():
            return True
        return False
    
    class Meta:
        ordering = ['-date', '-start_time']
        verbose_name = "Reunion"
        verbose_name_plural = "Reunions"


class ReminderLog(models.Model):
    """
    Model to track sent reminders for audit purposes
    """
    reunion = models.ForeignKey(Reunion, on_delete=models.CASCADE, related_name='reminder_logs')
    sent_at = models.DateTimeField(auto_now_add=True)
    reminder_type = models.CharField(max_length=50, default="scheduled")
    sent_via = models.CharField(max_length=50, default="system", help_text="How the reminder was sent")
    status = models.CharField(max_length=20, default="sent", help_text="sent, failed, etc.")
    notes = models.TextField(blank=True, help_text="Additional information about the reminder")
    
    def __str__(self):
        return f"Reminder for {self.reunion.title} at {self.sent_at}"
    
    class Meta:
        ordering = ['-sent_at']
        verbose_name = "Reminder Log"
        verbose_name_plural = "Reminder Logs"