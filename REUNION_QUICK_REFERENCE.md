# REUNION SYSTEM - QUICK REFERENCE GUIDE

## URL Endpoints

### Meeting Management
- **List all meetings:** `/Reunion/`
- **View meeting details:** `/Reunion/<id>/`
- **Create new meeting:** `/Reunion/create/`
- **Edit meeting:** `/Reunion/<id>/update/`
- **Delete meeting:** `/Reunion/<id>/delete/`

### Reminder History
- **View reminder logs:** `/Reunion/reminders/`
- **View reminder details:** `/Reunion/reminders/<id>/`
- **Delete reminder log:** `/Reunion/reminders/<id>/delete/`

---

## Creating a Meeting - Step by Step

### Valid Example:
```
Title:           "Math Study Group"
Date:            2025-12-18 (tomorrow or later)
Start Time:      14:00
End Time:        15:30 (MUST be after start time)
Reunion Type:    "Revision with Classmates"
Subject:         "Mathematics"
Description:     "Preparing for midterm exam"
Reminder:        ✓ Enabled
Reminder Time:   30 minutes before
```

### Invalid Examples (Will Show Errors):
```
❌ Date: 2025-12-16 (yesterday) 
   → Error: "The meeting date cannot be in the past."

❌ Date: 2025-12-17 (today), Start Time: 10:00 (already passed)
   → Error: "The meeting start time cannot be in the past."

❌ Start Time: 15:00, End Time: 15:00 (same time)
   → Error: "The end time must be after the start time."

❌ Start Time: 15:00, End Time: 14:00 (end before start)
   → Error: "The end time must be after the start time."
```

---

## Error Messages & Solutions

### Meeting Date Errors
| Error | Cause | Solution |
|-------|-------|----------|
| "The meeting date cannot be in the past." | Selected a past date | Choose today or later |
| "The meeting start time cannot be in the past." | Today's date with past time | Choose a future time |

### Meeting Time Errors
| Error | Cause | Solution |
|-------|-------|----------|
| "The end time must be after the start time." | End time ≤ start time | Make end time later than start |

---

## Form Fields Explained

### Required Fields (*)
- **Title** - Brief name for the meeting (max 200 chars)
- **Date** - When the meeting happens
- **Start Time** - When meeting begins (24-hour format)
- **End Time** - When meeting ends (must be after start time)
- **Meeting Type** - Category of meeting
- **Subject** - Academic subject or topic

### Optional Fields
- **Description** - Additional details about meeting
- **Enable Reminder** - Get email before meeting
- **Reminder Timing** - How long before to send email

### Meeting Types
- Education Course
- Project Meeting
- Revision with Classmates
- Other

### Subject Options
- Mathematics
- Physics
- Computer Science
- Biology
- Chemistry
- Literature
- History
- Other

### Reminder Timing Options
- 5 minutes before
- 15 minutes before
- 30 minutes before (default)
- 1 hour before
- 2 hours before
- 1 day before
- 2 days before

---

## Features Overview

### 📧 Email System
✅ **ON CREATION:** Emails sent to all active users
✅ **REMINDERS:** Emails sent at configured time before meeting
✅ **PRIVACY:** All recipient emails hidden using BCC

### 🔄 Auto-Recurring Meetings
✅ **AUTOMATIC:** New meeting created 7 days later
✅ **SAME SETTINGS:** All details copied to new meeting
✅ **SMART:** Won't create if already exists for next week

### 📝 Validation
✅ **DATE:** Rejects past dates
✅ **TIME:** Rejects past times for today
✅ **RANGE:** Ensures end time > start time
✅ **ERROR DISPLAY:** Shows errors in red on form

### 📊 Tracking
✅ **REMINDER LOGS:** All sent reminders tracked
✅ **HISTORY:** View when each reminder was sent
✅ **STATUS:** Can see if reminder sent successfully

---

## Testing Checklist

### Manual Testing
- [ ] Create meeting with valid data → Check email
- [ ] Try past date → See error message
- [ ] Try invalid time range → See error message
- [ ] Edit existing meeting → Verify updates save
- [ ] Delete meeting → Verify confirmation works
- [ ] Filter by upcoming/past → Verify filtering works
- [ ] Search by title → Verify search works
- [ ] View meeting details → Verify all info displays

### What to Check After Submit
1. ✓ Form submitted successfully?
2. ✓ Redirected to meeting list?
3. ✓ New meeting appears in list?
4. ✓ Email received by all users?
5. ✓ Meeting details correct?

---

## Common Issues & Solutions

### Issue: Form Shows No Errors
**Solution:** Check browser console for JavaScript errors

### Issue: Email Not Received
**Solution:** 
1. Check email backend is configured in settings.py
2. Check email address is valid
3. Check user is marked as active in database
4. Check spam folder
5. Check email logs in Django admin

### Issue: Reminder Never Sent
**Solution:**
1. Scheduler (Celery/Cron) must be running
2. send_reminders() function must be scheduled
3. Check scheduler logs for errors

### Issue: Past Date Accepted
**Solution:** Server time may be out of sync - check server timezone in settings.py

---

## Admin Interface

Access Django Admin: `/admin/`

### Manage Reunions
1. Go to Reunion > Reunions
2. Can view, edit, delete meetings
3. Can create meetings with all validations applied

### Manage Reminder Logs
1. Go to Reunion > Reminder Logs
2. Can view all sent reminders
3. Can see delivery status

---

## Configuration Required

### Email Setup (settings.py)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

### Scheduler Setup
```bash
# Every 5 minutes - send reminders
*/5 * * * * cd /path/to/project && python manage.py send_reminders

# Every 1 minute - create recurring meetings
*/1 * * * * cd /path/to/project && python manage.py auto_generate_recurring_meetings
```

---

## Database Schema

### Reunion Model
```
id (Primary Key)
title (CharField, max 200) *
date (DateField) *
start_time (TimeField) *
end_time (TimeField) *
reunion_type (CharField, choices) *
subject (CharField, choices) *
description (TextField)
reminder_enabled (BooleanField, default True)
reminder_timing (IntegerField, choices)
reminder_sent (BooleanField, default False)
reminder_sent_at (DateTimeField, nullable)
organizer (ForeignKey to User)
created_at (DateTimeField, auto_now_add)
updated_at (DateTimeField, auto_now)
```

### ReminderLog Model
```
id (Primary Key)
reunion (ForeignKey)
sent_at (DateTimeField, auto_now_add)
reminder_type (CharField)
sent_via (CharField)
status (CharField: sent, failed, etc)
notes (TextField)
```

---

## API for Developers

### Create Meeting via Django Shell
```python
from Reunion.models import Reunion
from django.contrib.auth import get_user_model
from datetime import date, time

User = get_user_model()
user = User.objects.first()

meeting = Reunion.objects.create(
    title="My Meeting",
    date=date(2025, 12, 18),
    start_time=time(14, 0),
    end_time=time(15, 0),
    reunion_type='project',
    subject='math',
    organizer=user
)
```

### Send Reminders Manually
```python
from Reunion.cron import send_reminders
send_reminders()
```

### Generate Recurring Meetings Manually
```python
from Reunion.cron import auto_generate_recurring_meetings
auto_generate_recurring_meetings()
```

---

## Key Files to Review

1. **Models:** `Reunion/models.py`
2. **Views:** `Reunion/views.py`
3. **Forms:** `Reunion/forms.py`
4. **Signals:** `Reunion/signals.py`
5. **Cron:** `Reunion/cron.py`
6. **Templates:** `templates/base_tailwind/reunion_*.html`
7. **Tests:** `test_reunion_functions.py`

---

## Status: ✅ FULLY OPERATIONAL

All features working and tested:
- ✅ CRUD Operations
- ✅ Input Validation with HTML Error Display
- ✅ Email on Meeting Creation
- ✅ Email Reminders (Requires Scheduler)
- ✅ Auto-Recurring Meetings (Requires Scheduler)
- ✅ Reminder Logging & Tracking

**Generated:** December 17, 2025
