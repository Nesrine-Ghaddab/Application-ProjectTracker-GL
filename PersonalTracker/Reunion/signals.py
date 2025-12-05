# Reunion/signals.py
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from .models import Reunion

@receiver(post_save, sender=Reunion)
def send_reunion_created_email(sender, instance, created, **kwargs):
    """
    When a Reunion is created we email all active users.
    Uses Django email backend. Switch to Resend API later if you prefer.
    """
    if not created:
        return  # only send on creation

    # collect recipient addresses (only users with valid email)
    User = get_user_model()
    recipients_qs = User.objects.filter(is_active=True).exclude(email__isnull=True).exclude(email__exact="")
    recipient_emails = list(recipients_qs.values_list("email", flat=True))
    if not recipient_emails:
        # nothing to do
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"No active users with email found for reunion '{instance.title}'")
        return

    # prepare subject and rendered bodies
    subject = f"New Reunion: {instance.title} — {instance.date}"
    # You can create templates reminder_email.txt and reminder_email.html in Reunion/templates/
    context = {"reunion": instance, "site_name": getattr(settings, "SITE_NAME", "PersonalTracker")}
    text_body = render_to_string("reminder_email.txt", context)
    html_body = render_to_string("reminder_email.html", context)

    # send using BCC to avoid exposing everyone's email. For small lists this is fine.
    msg = EmailMultiAlternatives(subject=subject,
                                 body=text_body,
                                 from_email=settings.DEFAULT_FROM_EMAIL,
                                 bcc=recipient_emails)
    msg.attach_alternative(html_body, "text/html")
    try:
        msg.send(fail_silently=False)
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Reunion created email sent to {len(recipient_emails)} active users for '{instance.title}'")
    except Exception:
        # optionally log error rather than crash
        import logging
        logger = logging.getLogger(__name__)
        logger.exception("Failed to send reunion-created emails")
