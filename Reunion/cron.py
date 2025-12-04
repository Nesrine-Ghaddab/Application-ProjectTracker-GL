# Reunion/cron.py
import logging
from datetime import timedelta
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from .models import Reunion, ReminderLog

logger = logging.getLogger(__name__)

def get_active_user_emails():
    """Return list of all active users' emails."""
    User = get_user_model()
    return list(User.objects.filter(is_active=True).exclude(email__isnull=True).exclude(email__exact="").values_list("email", flat=True))

def send_reminder_for(reunion, recipients):
    """Send reminder email for a reunion to specified recipients."""
    subject = f"Reminder: {reunion.title} on {reunion.date}"
    
    # Prepare email body
    context = {"reunion": reunion, "site_name": getattr(settings, "SITE_NAME", "PersonalTracker")}
    text_body = render_to_string("reminder_email.txt", context)
    html_body = render_to_string("reminder_email.html", context)
    
    # Use EmailMultiAlternatives for HTML support
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        bcc=recipients,  # Use BCC to protect privacy
    )
    msg.attach_alternative(html_body, "text/html")

    # send and return True/False
    try:
        msg.send(fail_silently=False)
        logger.info("Reminder email sent successfully for reunion id=%s to %d recipients", reunion.id, len(recipients))
        return True
    except Exception as e:
        logger.exception("Failed to send reminder for reunion id=%s: %s", reunion.id, str(e))
        return False

def send_reminders():
    """Send reminders for upcoming reunions to all active users."""
    logger.info("send_reminders started")
    now = timezone.localtime()  # match how your model computes reminder_datetime
    due_qs = Reunion.objects.filter(reminder_enabled=True, reminder_sent=False)

    # Get all active user emails once
    recipients = get_active_user_emails()
    
    if not recipients:
        logger.warning("No active users with email found. Skipping reminder sending.")
        return

    for r in due_qs:
        # skip null reminder_datetime
        if r.reminder_datetime is None:
            logger.info("Skipping (no reminder_datetime) -> %s (id=%s)", r.title, r.id)
            continue

        # If reminder_datetime already passed or due now
        if r.reminder_datetime <= now:
            ok = send_reminder_for(r, recipients)
            if ok:
                r.reminder_sent = True
                r.reminder_sent_at = timezone.now()
                r.save(update_fields=["reminder_sent", "reminder_sent_at"])
                logger.info("Reminder sent for %s (id=%s) -> %d active users", r.title, r.id, len(recipients))
            else:
                logger.warning("Reminder failed for %s (id=%s). Will retry on next run.", r.title, r.id)
        else:
            logger.debug("Skipping (no need) -> %s - %s", r.title, r.reminder_datetime)

    logger.info("send_reminders finished")

def auto_generate_recurring_meetings():
    """
    Automatically generate recurring meetings for the next week
    when a meeting has passed (reminder sent and end time passed).
    """
    logger.info("auto_generate_recurring_meetings started")
    now = timezone.now()
    
    # Find meetings that have:
    # 1. Had their reminder sent
    # 2. End time has passed
    # 3. Don't already have a recurring meeting created for next week
    
    past_meetings = Reunion.objects.filter(
        reminder_sent=True,
        date__lt=now.date()  # Meeting date is in the past
    )
    
    for meeting in past_meetings:
        # Check if end time has actually passed
        meeting_end_datetime = timezone.make_aware(
            timezone.datetime.combine(meeting.date, meeting.end_time)
        )
        
        if meeting_end_datetime >= now:
            continue  # Not fully passed yet
        
        # Check if a recurring meeting for next week already exists
        next_week_date = meeting.date + timedelta(days=7)
        next_week_meeting = Reunion.objects.filter(
            title__icontains=meeting.title,
            date=next_week_date,
            start_time=meeting.start_time,
            end_time=meeting.end_time
        ).exists()
        
        if next_week_meeting:
            logger.info("Recurring meeting already exists for %s on %s", meeting.title, next_week_date)
            continue
        
        # Create the recurring meeting for next week
        try:
            new_meeting = Reunion.objects.create(
                title=meeting.title,
                description=meeting.description,
                date=next_week_date,
                start_time=meeting.start_time,
                end_time=meeting.end_time,
                reunion_type=meeting.reunion_type,
                subject=meeting.subject,
                reminder_enabled=meeting.reminder_enabled,
                reminder_timing=meeting.reminder_timing
            )
            logger.info(
                "✓ Auto-generated recurring meeting: %s on %s (ID: %s -> ID: %s)",
                new_meeting.title,
                new_meeting.date,
                meeting.id,
                new_meeting.id
            )
        except Exception as e:
            logger.exception(
                "Failed to auto-generate recurring meeting for %s: %s",
                meeting.title,
                str(e)
            )
    
    logger.info("auto_generate_recurring_meetings finished")
