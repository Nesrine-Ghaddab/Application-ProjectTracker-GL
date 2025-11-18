# SessionApp/views.py
import json
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import StudySession
from .forms import StudySessionForm


# ========== PAGES ==========

def landing(request):
    return render(request, "base_tailwind/index.html")


@login_required
def home(request):
    """Dashboard sessions + timer (sessions.html)."""
    running = StudySession.objects.filter(user=request.user, is_running=True).first()
    suggestion = StudySession.suggest_duration_for_user(request.user)
    streak = StudySession.streak_for_user(request.user)

    today = timezone.localdate()
    start_week = today - timedelta(days=6)
    qs = StudySession.objects.filter(user=request.user).order_by("-started_at")

    # stats: on compte seulement les sessions terminées
    today_minutes = sum(
        s.duration_seconds
        for s in qs
        if s.started_at.date() == today and not s.is_running
    ) // 60

    week_minutes = sum(
        s.duration_seconds
        for s in qs
        if s.started_at.date() >= start_week and not s.is_running
    ) // 60

    recent = list(
        qs.values("id", "title", "duration_seconds", "started_at", "is_running")[:10]
    )
    for r in recent:
        r["duration_minutes"] = (
            round(r["duration_seconds"] / 60, 1) if r["duration_seconds"] else 0
        )

    context = {
        "running": running,
        "suggestion": suggestion,
        "streak": streak,
        "today_minutes": today_minutes,
        "week_minutes": week_minutes,
        "recent_json": json.dumps(recent, default=str),
        "display_name": request.user.get_username() or "Utilisateur",
    }
    # 👉 ton nouveau template
    return render(request, "base_tailwind/sessions.html", context)


# ========== API TIMER ==========

@login_required
@require_POST
def api_session_start(request):
    if StudySession.objects.filter(user=request.user, is_running=True).exists():
        return HttpResponseBadRequest("Une session est déjà en cours.")
    title = (request.POST.get("title") or "").strip()
    planned = int(request.POST.get("planned_minutes") or 50)
    brk = int(request.POST.get("break_minutes") or 10)
    s = StudySession.objects.create(
        user=request.user,
        title=title,
        planned_minutes=planned,
        break_minutes=brk,
        started_at=timezone.now(),
        is_running=True,
    )
    return JsonResponse({"ok": True, "session_id": s.id})


@login_required
@require_POST
def api_session_stop(request):
    sid = request.POST.get("session_id")
    if not sid:
        return HttpResponseBadRequest("session_id manquant.")
    s = get_object_or_404(StudySession, pk=sid, user=request.user, is_running=True)
    s.stop()
    s.save()
    return JsonResponse({"ok": True, "duration_seconds": s.duration_seconds})


@login_required
def api_recent_sessions(request):
    recent = list(
        StudySession.objects.filter(user=request.user)
        .order_by("-started_at")
        .values("id", "title", "duration_seconds", "started_at", "is_running")[:10]
    )
    for r in recent:
        r["duration_minutes"] = (
            round(r["duration_seconds"] / 60, 1) if r["duration_seconds"] else 0
        )
    return JsonResponse({"items": recent})


@login_required
def api_summary(request):
    today = timezone.localdate()
    start_week = today - timedelta(days=6)
    qs = StudySession.objects.filter(user=request.user).order_by("-started_at")

    today_minutes = sum(
        s.duration_seconds
        for s in qs
        if s.started_at.date() == today and not s.is_running
    ) // 60
    week_minutes = sum(
        s.duration_seconds
        for s in qs
        if s.started_at.date() >= start_week and not s.is_running
    ) // 60
    streak = StudySession.streak_for_user(request.user)

    recent = list(
        qs.values("id", "title", "duration_seconds", "started_at", "is_running")[:10]
    )
    for r in recent:
        r["duration_minutes"] = (
            round(r["duration_seconds"] / 60, 1) if r["duration_seconds"] else 0
        )

    return JsonResponse(
        {
            "today_minutes": today_minutes,
            "week_minutes": week_minutes,
            "streak": streak,
            "recent": recent,
        }
    )


# ========== CRUD ==========

@login_required
def session_list(request):
    sessions = (
        StudySession.objects
        .filter(user=request.user)
        .order_by('-started_at')
    )
    return render(request, "base_tailwind/sessions_history.html", {
        "sessions": sessions,
    })


@login_required
def session_create(request):
    if request.method == "POST":
        form = StudySessionForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect("study:session_list")
    else:
        form = StudySessionForm(initial={"started_at": timezone.now()})
    return render(
        request,
        "study/session_form.html",
        {"form": form, "mode": "create"},
    )


@login_required
def session_update(request, pk):
    session = get_object_or_404(StudySession, pk=pk, user=request.user)

    if request.method == "POST":
        form = StudySessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect("study:session_list")
    else:
        form = StudySessionForm(instance=session)

    return render(request, "base_tailwind/session_form.html", {"form": form})



@login_required
@require_POST
def session_delete(request, pk: int):
    s = get_object_or_404(StudySession, pk=pk, user=request.user)
    s.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/sessions/"))
@login_required
@require_POST
def session_rename(request, pk):
    """Met à jour uniquement le titre d'une session (appelé en AJAX)."""
    session = get_object_or_404(StudySession, pk=pk, user=request.user)
    title = (request.POST.get("title") or "").strip()
    session.title = title
    session.save(update_fields=["title", "updated_at"])

    # Si c'est un appel AJAX on renvoie du JSON
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"ok": True, "title": session.title})

    # fallback, au cas où
    return redirect("study:session_list")