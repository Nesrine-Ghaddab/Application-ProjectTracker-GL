from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Project, Task
from .forms import ProjectForm, TaskForm, ProjectUpdateForm
from django.utils import timezone
from django.contrib.auth import logout
from datetime import timedelta, date
from django.db.models import Avg, Count
from datetime import date
from .models import Project
from datetime import date
from .models import Project, Notification

def check_deadlines(user):
    overdue_projects = Project.objects.filter(deadline__lt=date.today())

    for project in overdue_projects:
        # éviter duplicates
        notif_exists = Notification.objects.filter(
            user=user,
            message__icontains=project.title
        ).exists()

        if not notif_exists:
            Notification.objects.create(
                user=user,
                message=f"Le projet '{project.title}' a dépassé sa deadline."
            )
def mark_as_read(request, notif_id):
    notif = Notification.objects.get(id=notif_id, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect("dashboard")

def overdue_projects(request):
    overdue = Project.objects.filter(deadline__lt=date.today())
    return render(request, "ton_template.html", {
        "overdue_projects": overdue
    })
def dashboard(request):
    check_deadlines(request.user)

    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    return render(request, "dashboard.html", {
        "notifications": notifications,
    })

def project_list(request):
    """Lister tous les projets (sans user)"""
    projects = Project.objects.all()
    notifications = Notification.objects.all().order_by('-created_at')  # fetch all

    # Filtres
    status_filter = request.GET.get('status', '')
    if status_filter:
        projects = projects.filter(status=status_filter)

    # Recherche
    search_query = request.GET.get('search', '')
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Tri
    sort_by = request.GET.get('sort', '-created_at')
    valid_sort_fields = [
        'title', '-title', 'deadline', '-deadline',
        'status', '-status', 'progress', '-progress',
        'created_at', '-created_at'
    ]
    if sort_by in valid_sort_fields:
        projects = projects.order_by(sort_by)

    # === Statistiques ===
    stats = {
        "total_projects": projects.count(),
        "completed_projects": projects.filter(status="completed").count(),
        "in_progress_projects": projects.filter(status="in_progress").count(),
        "average_progress": projects.aggregate(avg=Avg("progress"))["avg"] or 0,
    }

    context = {
        'projects': projects,
        'current_filter': status_filter,
        'search_query': search_query,
        'current_sort': sort_by,
        "stats": stats,
        'notifications': notifications,
        'current_filter': request.GET.get('status', ''),
        'search_query': request.GET.get('search', ''),
        'current_sort': request.GET.get('sort', '-created_at'),

    }
    

    return render(request, 'base_tailwind/project_list.html', context)

def project_create(request):
    """Créer un nouveau projet (aucune auth nécessaire)"""
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            messages.success(request, f'Projet "{project.title}" créé avec succès !')
            return redirect('Gestion_Projects:project_detail', pk=project.pk)
    else:
        form = ProjectForm()

    return render(request, 'base_tailwind/project_form.html', {
        'form': form,
        'title': 'Créer un projet'
    })


def project_detail(request, pk):
    """Afficher les détails d'un projet (public)"""
    project = get_object_or_404(Project, pk=pk)
    tasks = project.tasks.all()

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(is_completed=True).count()
    pending_tasks = total_tasks - completed_tasks

    context = {
        'project': project,
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
    }
    return render(request, 'base_tailwind/project_detail.html', context)

def project_update(request, pk):
    """Modifier un projet (aucune auth)"""
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        form = ProjectUpdateForm(request.POST, instance=project)
        if form.is_valid():
            old_deadline = project.deadline
            project = form.save()

            if old_deadline != project.deadline:
                updated, overdue = _recalculate_task_deadlines(project)
                messages.info(request, f'{updated} tâches recalculées')
                if overdue:
                    messages.warning(request, f'{overdue} tâches en retard')

            messages.success(request, f'Projet "{project.title}" modifié !')
            return redirect('Gestion_Projects:project_detail', pk=project.pk)
    else:
        form = ProjectUpdateForm(instance=project)

    return render(request, 'base_tailwind/project_form.html', {
        'form': form,
        'title': 'Modifier le projet',
        'project': project,
    })

    
def project_delete(request, pk):
    """Supprimer un projet (public)"""
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        project_title = project.title
        project.delete()
        messages.success(request, f'Projet "{project_title}" supprimé !')
        return redirect('Gestion_Projects:project_list')

    return render(request, 'base_tailwind/project_confirm_delete.html', {
        'project': project
    })



def logout_view(request):
    """Logout the current user and redirect to login page."""
    if request.method == 'POST':
        logout(request)
        messages.info(request, "Vous êtes déconnecté.")
        return redirect('login')
    return redirect('Gestion_Projects:project_list')


def _recalculate_task_deadlines(project):
    tasks = list(project.tasks.filter(is_completed=False).order_by('deadline', 'created_at'))
    if not tasks:
        return 0, 0

    today = date.today()
    end = project.deadline
    if end < today:
        end = today

    total_days = max(0, (end - today).days)

    weight_map = {'high': 3, 'medium': 2, 'low': 1}
    weights = [weight_map.get(t.priority, 2) for t in tasks]
    total_weight = sum(weights)

    updated = 0
    overdue = 0
    cumulative = 0

    for idx, task in enumerate(tasks):
        cumulative += weights[idx]
        pos = cumulative / total_weight if total_weight > 0 else (idx + 1) / len(tasks)
        days_offset = round(pos * total_days)
        new_deadline = today + timedelta(days=days_offset)

        if new_deadline > project.deadline:
            new_deadline = project.deadline

        if task.deadline != new_deadline:
            task.deadline = new_deadline
            task.save()
            updated += 1

        if task.deadline < today and not task.is_completed:
            overdue += 1

    return updated, overdue
