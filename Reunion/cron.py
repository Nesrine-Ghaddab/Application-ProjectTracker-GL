from django.utils import timezone
from .models import Reunion, ReminderLog

def send_reminders():
    now = timezone.now()
    
    meetings = Reunion.objects.filter(
        reminder_enabled=True,
        reminder_sent=False
    )

    for meeting in meetings:
        if meeting.needs_reminder:

            # HERE you send an email or notification
            # (fake example)
            print(f"Reminder for: {meeting.title}")

            meeting.reminder_sent = True
            meeting.reminder_sent_at = now
            meeting.save()

            ReminderLog.objects.create(
                reunion=meeting,
                reminder_type="auto",
                sent_via="system",
                status="sent"
            )
            print("Reminder for:", meeting.title)
        else:
            print("No reminder needed for:", meeting.title)