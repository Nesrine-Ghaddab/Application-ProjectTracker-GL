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

@login_required
def project_list(request):
    """1.2 - Lister tous les projets"""
    projects = Project.objects.filter(user=request.user)
    
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
    sort_by = request.GET.get('sort', '-created_at')  # Par défaut: plus récent d'abord
    valid_sort_fields = ['title', '-title', 'deadline', '-deadline', 'status', '-status',
                        'progress', '-progress', 'created_at', '-created_at']
    if sort_by in valid_sort_fields:
        projects = projects.order_by(sort_by)
    
    context = {
        'projects': projects,
        'current_filter': status_filter,
        'search_query': search_query,
        'current_sort': sort_by,
    }
    return render(request, 'base_tailwind/project_list.html', context)

@login_required
def project_create(request):
    """1.1 - Créer un nouveau projet"""
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            messages.success(request, f'Le projet "{project.title}" a été créé avec succès!')
            return redirect('Gestion_Projects:project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    
    return render(request, 'base_tailwind/project_form.html', {
        'form': form,
        'title': 'Créer un projet'
    })

@login_required
def project_detail(request, pk):
    """1.2 - Afficher les détails d'un projet"""
    project = get_object_or_404(Project, pk=pk, user=request.user)
    tasks = project.tasks.all()
    
    # Statistiques des tâches
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

@login_required
def project_update(request, pk):
    """1.3 - Modifier un projet et 1.4 - Recalculer les délais"""
    project = get_object_or_404(Project, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ProjectUpdateForm(request.POST, instance=project)
        if form.is_valid():
            old_deadline = project.deadline
            project = form.save()
            
            # 1.4 - Vérifier si la deadline a changé
            if old_deadline != project.deadline:
                messages.warning(request, 
                    f'La deadline a été modifiée. Nouvelle date: {project.deadline}.'
                )
                # Recalculate task deadlines and report changes
                updated_count, overdue_count = _recalculate_task_deadlines(project)
                if updated_count:
                    messages.info(request, f'{updated_count} tâche(s) ont été réordonnées en fonction de la nouvelle deadline.')
                if overdue_count:
                    messages.error(request, f'Attention : {overdue_count} tâche(s) sont maintenant en retard.')
            
            messages.success(request, f'Le projet "{project.title}" a été modifié avec succès!')
            return redirect('Gestion_Projects:project_detail', pk=project.pk)
    else:
        form = ProjectUpdateForm(instance=project)
    
    return render(request, 'base_tailwind/project_form.html', {
        'form': form,
        'title': 'Modifier le projet',
        'project': project,
    })

@login_required
def project_delete(request, pk):
    """1.5 - Supprimer un projet"""
    project = get_object_or_404(Project, pk=pk, user=request.user)
    
    if request.method == 'POST':
        project_title = project.title
        project.delete()
        messages.success(request, f'Le projet "{project_title}" a été supprimé avec succès!')
        return redirect('Gestion_Projects:project_list')
    
    return render(request, 'base_tailwind/project_confirm_delete.html', {
        'project': project
    })


def logout_view(request):
    """Logout the current user and redirect to login page.

    For safety we only perform logout on POST requests. GET requests will
    simply redirect back to the project list (no message) to avoid accidental
    logouts (for example from prefetching or bots).
    """
    if request.method == 'POST':
        logout(request)
        messages.info(request, "Vous êtes déconnecté.")
        return redirect('logout')
    # If accessed by GET, don't log out — just redirect to projects list
    return redirect('Gestion_Projects:project_list')


def _recalculate_task_deadlines(project):
    """Recalculate deadlines for tasks of a project when the project deadline changes.

    Strategy:
    - Compute the available window from today (or earliest task date) to project.deadline.
    - Distribute tasks within that window according to priority weights so higher priority tasks
      get earlier slots.
    - If the new project deadline is in the past, set tasks' deadlines to today (so they appear overdue).
    Returns a tuple (updated_count, overdue_count).
    """
    tasks = list(project.tasks.filter(is_completed=False).order_by('deadline', 'created_at'))
    if not tasks:
        return 0, 0

    today = date.today()
    end = project.deadline
    # If deadline is before today, set end to today to avoid negative windows
    if end < today:
        end = today

    total_days = max(0, (end - today).days)

    # Priority weighting: high=3, medium=2, low=1
    weight_map = {'high': 3, 'medium': 2, 'low': 1}
    weights = [weight_map.get(t.priority, 2) for t in tasks]
    total_weight = sum(weights)

    updated = 0
    overdue = 0

    # Cumulative allocation
    cumulative = 0
    for idx, task in enumerate(tasks):
        w = weights[idx]
        cumulative += w
        # proportional position in (0, total_days]
        if total_weight > 0:
            pos = cumulative / total_weight
        else:
            pos = (idx + 1) / len(tasks)

        # assign deadline
        days_offset = round(pos * total_days)
        new_deadline = today + timedelta(days=days_offset)
        # ensure not beyond project.deadline
        if new_deadline > project.deadline:
            new_deadline = project.deadline

        if task.deadline != new_deadline:
            task.deadline = new_deadline
            task.save()
            updated += 1

        if task.deadline < date.today() and not task.is_completed:
            overdue += 1

    return updated, overdue