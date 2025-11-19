# Reunion/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Reunion, ReminderLog
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

class ReunionList(ListView):
    model = Reunion
    context_object_name = "reunions"
    ordering = ["-date", "-start_time"]
    template_name = "meeting.html"  # Make sure this matches your actual file name

class ReunionDetail(DetailView):
    model = Reunion
    template_name = "reunion_detail.html"
    context_object_name = "reunion"

class ReunionCreate(CreateView):
    model = Reunion
    template_name = "reunion_form.html"
    fields = [
        'title', 'date', 'start_time', 'end_time', 'reunion_type', 
        'subject', 'description', 'reminder_enabled', 'reminder_timing'
    ]
    success_url = reverse_lazy("reunion_list")

class ReunionUpdate(UpdateView):
    model = Reunion
    template_name = "reunion_form.html"
    fields = [
        'title', 'date', 'start_time', 'end_time', 'reunion_type', 
        'subject', 'description', 'reminder_enabled', 'reminder_timing'
    ]
    success_url = reverse_lazy("reunion_list")

class ReunionDelete(DeleteView):
    model = Reunion
    template_name = "reunion_confirm_delete.html"
    success_url = reverse_lazy("reunion_list")

class ReminderLogList(ListView):
    model = ReminderLog
    context_object_name = "reminder_logs"
    ordering = ["-sent_at"]
    template_name = "reminderlog_list.html"

class ReminderLogDetail(DetailView):
    model = ReminderLog
    template_name = "reminderlog_detail.html"
    context_object_name = "reminder_log"

class ReminderLogDelete(DeleteView):
    model = ReminderLog
    template_name = "reminderlog_confirm_delete.html"
    success_url = reverse_lazy("reminderlog_list")