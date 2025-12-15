import os
import resend
from django.conf import settings

def send_email_resend(subject, body, to_emails):
    """
    Sends email using Resend API.
    Returns (success_bool, message)
    """

    if not settings.RESEND_ENABLED:
        return False, "Resend disabled"

    if not settings.RESEND_API_KEY:
        return False, "No API key provided"

    resend.api_key = settings.RESEND_API_KEY

    try:
        result = resend.Emails.send({
            "from": settings.RESEND_FROM_EMAIL,
            "to": to_emails,
            "subject": subject,
            "html": f"<p>{body}</p>",
        })
        return True, f"sent via Resend: {result}"
    except Exception as e:
        return False, f"Resend error: {e}"
