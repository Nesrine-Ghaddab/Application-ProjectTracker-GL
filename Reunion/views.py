# Reunion/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Reunion, ReminderLog
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.db.models import Q

class ReunionList(ListView):
    model = Reunion
    context_object_name = "reunions"
    ordering = ["date", "start_time"]
    template_name = "meeting.html"

    def get_queryset(self):
        """Filter reunions based on search and filter parameters"""
        queryset = Reunion.objects.all()
        
        # Get filter type from GET parameters
        filter_type = self.request.GET.get('filter', 'all')
        now = timezone.now()
        
        if filter_type == 'upcoming':
            # Only show meetings that are in the future (after current date and time)
            queryset = queryset.filter(
                date__gt=now.date()
            ) | queryset.filter(
                date=now.date(),
                start_time__gt=now.time()
            )
        elif filter_type == 'past':
            # Only show meetings that are in the past (before current date and time)
            queryset = queryset.filter(
                date__lt=now.date()
            ) | queryset.filter(
                date=now.date(),
                start_time__lte=now.time()
            )
        
        # Get search query from GET parameters
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(subject__icontains=search_query) |
                Q(reunion_type__icontains=search_query)
            )
        
        # Get reunion type filter
        reunion_type = self.request.GET.get('reunion_type', '').strip()
        if reunion_type:
            queryset = queryset.filter(reunion_type=reunion_type)
        
        # Order by date and time (most recent first)
        return queryset.order_by("-date", "-start_time")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        
        # Get upcoming reunions for sidebar
        context["upcoming_reunions"] = (
            Reunion.objects
            .filter(date__gte=now.date())
            .order_by("date", "start_time")[:3]
        )
        
        # Pass current filter and search to template
        context["current_filter"] = self.request.GET.get('filter', 'all')
        context["search_query"] = self.request.GET.get('search', '')
        
        return context

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
    
    def form_valid(self, form):
        """Validate the form before saving"""
        try:
            form.instance.full_clean()  # This calls the clean() method
        except Exception as e:
            # If validation fails, add errors to form and return invalid
            for field, error in e.message_dict.items() if hasattr(e, 'message_dict') else []:
                form.add_error(field, error)
            return self.form_invalid(form)
        
        return super().form_valid(form)

class ReunionUpdate(UpdateView):
    model = Reunion
    template_name = "reunion_form.html"
    fields = [
        'title', 'date', 'start_time', 'end_time', 'reunion_type', 
        'subject', 'description', 'reminder_enabled', 'reminder_timing'
    ]
    success_url = reverse_lazy("reunion_list")
    
    def form_valid(self, form):
        """Validate the form before saving"""
        try:
            form.instance.full_clean()  # This calls the clean() method
        except Exception as e:
            # If validation fails, add errors to form and return invalid
            for field, error in e.message_dict.items() if hasattr(e, 'message_dict') else []:
                form.add_error(field, error)
            return self.form_invalid(form)
        
        return super().form_valid(form)

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