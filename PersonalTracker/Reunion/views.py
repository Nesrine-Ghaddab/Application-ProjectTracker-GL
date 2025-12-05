# Reunion/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Reunion, ReminderLog
from .forms import ReunionForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin

class ReunionList(LoginRequiredMixin,ListView):
    model = Reunion
    context_object_name = "reunions"
    ordering = ["date", "start_time"]
    template_name = "base_tailwind/meeting.html"

    def get_queryset(self):
        """Filter reunions based on search and filter parameters"""
        queryset = Reunion.objects.all()

        # Get filter type from GET parameters
        filter_type = self.request.GET.get('filter', 'all')
        now = timezone.localtime()
        today = now.date()
        time_now = now.time()
        
        if filter_type == 'upcoming':
            q = Q(date__gt=today) | (Q(date=today) & Q(start_time__gt=time_now))
            queryset = queryset.filter(q)
        elif filter_type == 'past':
            q = Q(date__lt=today) | (Q(date=today) & Q(start_time__lte=time_now))
            queryset = queryset.filter(q)
        
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
        now = timezone.localtime()

        # Get upcoming reunions for sidebar
        context["upcoming_reunions"] = (
            Reunion.objects
            .filter(Q(date__gt=now.date()) | (Q(date=now.date()) & Q(start_time__gt=now.time())))
            .order_by("date", "start_time")[:3]
        )
        
        # Pass current filter and search to template
        context["current_filter"] = self.request.GET.get('filter', 'all')
        context["search_query"] = self.request.GET.get('search', '')
        
        return context

class ReunionDetail(LoginRequiredMixin , DetailView):
    model = Reunion
    template_name = "base_tailwind/reunion_detail.html"
    context_object_name = "reunion"

class ReunionCreate(LoginRequiredMixin, CreateView):
    model = Reunion
    form_class = ReunionForm
    template_name = "base_tailwind/reunion_form.html"
    success_url = reverse_lazy("reunion:list")
    
    def form_valid(self, form):
        """Validate the form before saving"""
        # Assign the current user to the organizer field
        form.instance.organizer = self.request.user
        print("Assigning organizer:", self.request.user)  # Debugging: Log the user assignment

        try:
            form.instance.full_clean()  # This calls the clean() method in the model
        except ValidationError as e:
            for field, errors in getattr(e, 'message_dict', {}).items():
                for error in errors:
                    form.add_error(field, error)
            print("Validation errors:", e.message_dict)  # Debugging: Log validation errors
            return self.form_invalid(form)

        return super().form_valid(form)

class ReunionUpdate(LoginRequiredMixin, UpdateView):
    model = Reunion
    form_class = ReunionForm
    template_name = "base_tailwind/reunion_form.html"
    success_url = reverse_lazy("reunion:list")
    
    def form_valid(self, form):
        """Validate the form before saving"""
        try:
            form.instance.full_clean()  # This calls the clean() method in the model
        except ValidationError as e:
            for field, errors in getattr(e, 'message_dict', {}).items():
                for error in errors:
                    form.add_error(field, error)
            return self.form_invalid(form)

        return super().form_valid(form)

class ReunionDelete(LoginRequiredMixin, DeleteView):
    model = Reunion
    template_name = "base_tailwind/reunion_confirm_delete.html"
    success_url = reverse_lazy("reunion:list")

class ReminderLogList(LoginRequiredMixin, ListView):
    model = ReminderLog
    context_object_name = "reminder_logs"
    ordering = ["-sent_at"]
    template_name = "base_tailwind/sessions_history.html"

class ReminderLogDetail(LoginRequiredMixin, DetailView):
    model = ReminderLog
    template_name = "base_tailwind/reunion_detail.html"
    context_object_name = "reminder_log"

class ReminderLogDelete(LoginRequiredMixin, DeleteView):
    model = ReminderLog
    template_name = "base_tailwind/reunion_confirm_delete.html"
    success_url = reverse_lazy("reunion:reminder_delete")