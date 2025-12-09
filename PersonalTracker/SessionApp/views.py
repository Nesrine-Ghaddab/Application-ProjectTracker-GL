# SessionApp/views.py
import json
from datetime import timedelta
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
    FileResponse,
)
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.urls import reverse

from reportlab.pdfgen import canvas

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

    # séries pour le graphique hebdomadaire (minutes par jour, Lun..Dim)
    week_series = [0] * 7  # index 0 = lundi, 6 = dimanche
    for s in qs:
        d = s.started_at.date()
        if d >= start_week and not s.is_running:
            wd = d.weekday()  # 0 = monday
            week_series[wd] += (s.duration_seconds or 0) // 60

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
        "week_series_json": json.dumps(week_series),
        "display_name": request.user.get_username() or "Utilisateur",
    }
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
    """Arrête la session et renvoie aussi l'URL du PDF généré."""
    sid = request.POST.get("session_id")
    if not sid:
        return HttpResponseBadRequest("session_id manquant.")

    s = get_object_or_404(
        StudySession, pk=sid, user=request.user, is_running=True
    )
    s.stop()
    s.save()

    pdf_url = reverse("study:session_pdf", args=[s.id])

    return JsonResponse(
        {
            "ok": True,
            "duration_seconds": s.duration_seconds,
            "pdf_url": pdf_url,
        }
    )


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


# ========== PDF ==========

@login_required
def session_pdf(request, pk):
    """Génère un PDF avec les détails d'une session."""
    session = get_object_or_404(StudySession, pk=pk, user=request.user)

    # On calcule l'heure de fin à partir de started_at + duration_seconds
    duration_sec = session.duration_seconds or 0
    finished_at = session.started_at + timedelta(seconds=duration_sec)

    # Buffer mémoire pour le PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    y = 800
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "Study session report")
    y -= 40

    p.setFont("Helvetica", 12)

    # Infos utilisateur / session
    p.drawString(50, y, f"User: {request.user.get_username()}")
    y -= 20

    p.drawString(50, y, f"Title: {session.title or 'Untitled session'}")
    y -= 20

    p.drawString(
        50,
        y,
        "Started at: "
        + timezone.localtime(session.started_at).strftime("%d/%m/%Y %H:%M"),
    )
    y -= 20

    p.drawString(
        50,
        y,
        "Finished at: "
        + timezone.localtime(finished_at).strftime("%d/%m/%Y %H:%M"),
    )
    y -= 20

    duration_min = duration_sec // 60
    p.drawString(50, y, f"Duration: {duration_min} minutes ({duration_sec} seconds)")
    y -= 20

    p.drawString(50, y, f"Planned focus: {session.planned_minutes} minutes")
    y -= 20

    p.drawString(50, y, f"Break: {session.break_minutes} minutes")
    y -= 40

    p.drawString(50, y, "Thank you for studying with Personal Tracker.")
    p.showPage()
    p.save()

    buffer.seek(0)
    filename = f"session-{session.id}.pdf"
    return FileResponse(buffer, as_attachment=True, filename=filename)


# ========== CRUD ==========

@login_required
def session_list(request):
    sessions = (
        StudySession.objects
        .filter(user=request.user)
        .order_by('-started_at')
    )

    # total duration for all sessions (in seconds)
    agg = sessions.aggregate(total_sec=Sum('duration_seconds'))
    total_seconds = agg['total_sec'] or 0

    # convert to hours / minutes
    total_hours = total_seconds // 3600
    total_minutes = (total_seconds % 3600) // 60

    return render(
        request,
        "base_tailwind/sessions_history.html",
        {
            "sessions": sessions,
            "total_hours": total_hours,
            "total_minutes": total_minutes,
        },
    )


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

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"ok": True, "title": session.title})

    return redirect("study:session_list")
