from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, TemplateView , ListView
from .models import Taches
from .forms import TachesForm
from datetime import date ,timedelta ,datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from django.utils import timezone
from Gestion_Projects.models import Project

# Détail d'une tâche
'''class TachesDetailView(DetailView):
    model = Taches
    template_name = 'base_tailwind/Taches_detail.html'
    context_object_name = 'tache' '''


class TachesDetailView(DetailView):
    model = Taches
    template_name = 'base_tailwind/Taches_detail.html'
    context_object_name = 'tache'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ajouter le projet lié à la tâche
        context['projet'] = self.object.projet
        return context



# Création d'une tâche
'''class TachesCreateView(CreateView):
    model = Taches
    form_class = TachesForm
    template_name = 'base_tailwind/Taches_form.html'
    success_url = reverse_lazy('Taches:frontoffice')'''
    
class TachesCreateView(CreateView):
    model = Taches
    form_class = TachesForm
    template_name = 'base_tailwind/Taches_form.html'

    def form_valid(self, form):
        projet_id = self.kwargs.get('projet_id')
        projet = get_object_or_404(Project, id=projet_id)
        form.instance.projet = projet
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('projects:project_detail', kwargs={'pk': self.object.projet.id})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projet_id = self.kwargs.get('projet_id')
        projet = get_object_or_404(Project, id=projet_id)
        context['projet'] = projet   
        return context


# Modification d'une tâche
class TachesUpdateView(UpdateView):
    model = Taches
    form_class = TachesForm
    template_name = 'base_tailwind/Taches_form.html'
    #success_url = reverse_lazy('Taches:frontoffice')
    def get_success_url(self):
        # On récupère le projet lié à la tâche supprimée
        projet_id = self.object.projet.id
        return reverse('Taches:project_taches', kwargs={'projet_id': projet_id})

# Suppression d'une tâche
class TachesDeleteView(DeleteView):
    model = Taches
    template_name = 'base_tailwind/Taches_confirm_delete.html'

    def get_success_url(self):
        # On récupère le projet lié à la tâche supprimée
        projet_id = self.object.projet.id
        return reverse('Taches:project_taches', kwargs={'projet_id': projet_id})


# Front office
"""
class FrontOfficeView(TemplateView):
    template_name = "base_tailwind/frontoffice.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        taches = Taches.objects.all()
        today = date.today()

        # Vérifier les deadlines
        for t in taches:
            if t.dateEcheance < today and t.statut != 'TERMINE':
                t.statut = 'TERMINE'
                t.resultat = 'ECHEC'
                t.save()

        context["taches"] = taches
        context["today"] = today
        return context
"""

class ProjectTachesListView(ListView):
    model = Taches
    template_name = 'base_tailwind/frontoffice.html'
    context_object_name = 'taches'
    
    def get_queryset(self):
        projet_id = self.kwargs.get('projet_id')
        return Taches.objects.filter(projet_id=projet_id)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projet_id = self.kwargs.get('projet_id')
        projet = get_object_or_404(Project, id=projet_id)
        context['projet'] = projet

        projet_id = self.kwargs.get('projet_id')
        projet = get_object_or_404(Project, id=projet_id)
        context['projet'] = projet
        # Récupérer toutes les tâches
        taches = Taches.objects.filter(projet=projet)
        today = date.today()
        
        # Vérifier et mettre à jour les deadlines dépassées
        for tache in taches:
            if tache.dateEcheance < today and tache.statut != 'TERMINE':
                tache.statut = 'TERMINE'
                tache.resultat = 'ECHEC'
                tache.save()
        
        # Calculer les dates de référence
        demain = today + timedelta(days=1)
        dans_2_jours = today + timedelta(days=2)
        
        # Tâches actives (non terminées)
        taches_actives = taches.exclude(statut='TERMINE')
        
        # Tâche la plus importante pour la notification
        tache_rappel_principale = None
        pourcentage_temps = 0
        
        if taches_actives.exists():
            # Trier par date d'échéance (la plus proche en premier)
            taches_triees = taches_actives.order_by('dateEcheance')
            tache_rappel_principale = taches_triees.first()
            
            # Calculer le pourcentage d'urgence
            pourcentage_temps = self._calculer_pourcentage_urgence(tache_rappel_principale, today)
        
        # Vérifier si la notification a été fermée
        notification_fermee = self.request.session.get('notification_fermee', False)
        
        # Préparer le contexte
        context.update({
            'taches': taches,
            'taches_actives': taches_actives,
            'tache_rappel_principale': tache_rappel_principale,
            'pourcentage_temps': pourcentage_temps,
            'today': today,
            'demain': demain,
            'dans_2_jours': dans_2_jours,
            'notification_fermee': notification_fermee,
        })
        
        return context
    def _calculer_pourcentage_urgence(self, tache, today):
        """Calcule le pourcentage d'urgence d'une tâche (0-100%)"""
        if not tache:
            return 0
        
        jours_restants = (tache.dateEcheance - today).days
        
        if jours_restants < 0:
            return 100
        elif jours_restants == 0:
            return 90
        elif jours_restants == 1:
            return 70
        elif jours_restants == 2:
            return 50
        elif jours_restants <= 7:
            return 30
        else:
            return 10
    
    def post(self, request, *args, **kwargs):
        """Gérer la fermeture et la réaffichage de la notification"""
        if 'fermer_notification' in request.POST:
            # Marquer la notification comme fermée
            request.session['notification_fermee'] = True
            request.session.modified = True
        
        if 'reafficher_notification' in request.POST:
            # Réafficher la notification
            if 'notification_fermee' in request.session:
                del request.session['notification_fermee']
            request.session.modified = True
        
        return redirect(reverse('Taches:project_taches', kwargs={'projet_id': self.kwargs.get('projet_id')}))

class FrontOfficeView(TemplateView):
    template_name = "base_tailwind/frontoffice.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        

        projet_id = self.kwargs.get('projet_id')
        projet = get_object_or_404(Project, id=projet_id)
        context['projet'] = projet
        # Récupérer toutes les tâches
        taches = Taches.objects.all()
        today = date.today()
        
        # Vérifier et mettre à jour les deadlines dépassées
        for tache in taches:
            if tache.dateEcheance < today and tache.statut != 'TERMINE':
                tache.statut = 'TERMINE'
                tache.resultat = 'ECHEC'
                tache.save()
        
        # Calculer les dates de référence
        demain = today + timedelta(days=1)
        dans_2_jours = today + timedelta(days=2)
        
        # Tâches actives (non terminées)
        taches_actives = taches.exclude(statut='TERMINE')
        
        # Tâche la plus importante pour la notification
        tache_rappel_principale = None
        pourcentage_temps = 0
        
        if taches_actives.exists():
            # Trier par date d'échéance (la plus proche en premier)
            taches_triees = taches_actives.order_by('dateEcheance')
            tache_rappel_principale = taches_triees.first()
            
            # Calculer le pourcentage d'urgence
            pourcentage_temps = self._calculer_pourcentage_urgence(tache_rappel_principale, today)
        
        # Vérifier si la notification a été fermée
        notification_fermee = self.request.session.get('notification_fermee', False)
        
        # Préparer le contexte
        context.update({
            'taches': taches,
            'taches_actives': taches_actives,
            'tache_rappel_principale': tache_rappel_principale,
            'pourcentage_temps': pourcentage_temps,
            'today': today,
            'demain': demain,
            'dans_2_jours': dans_2_jours,
            'notification_fermee': notification_fermee,
        })
        
        return context
    
    def _calculer_pourcentage_urgence(self, tache, today):
        """Calcule le pourcentage d'urgence d'une tâche (0-100%)"""
        if not tache:
            return 0
        
        jours_restants = (tache.dateEcheance - today).days
        
        if jours_restants < 0:
            return 100
        elif jours_restants == 0:
            return 90
        elif jours_restants == 1:
            return 70
        elif jours_restants == 2:
            return 50
        elif jours_restants <= 7:
            return 30
        else:
            return 10
    
    def post(self, request, *args, **kwargs):
        """Gérer la fermeture et la réaffichage de la notification"""
        if 'fermer_notification' in request.POST:
            # Marquer la notification comme fermée
            request.session['notification_fermee'] = True
            request.session.modified = True
        
        if 'reafficher_notification' in request.POST:
            # Réafficher la notification
            if 'notification_fermee' in request.session:
                del request.session['notification_fermee']
            request.session.modified = True
        
        return redirect('Taches:frontoffice')
    
    def _calculer_statistiques(self, taches, today):
        """Calcule les statistiques"""
        demain = today + timedelta(days=1)
        
        stats = {
            'total': len(taches),
            'termines': taches.filter(statut='TERMINE').count(),
            'en_cours': taches.filter(statut='EN_COURS').count(),
            'en_attente': taches.filter(statut='EN_ATTENTE').count(),
            'aujourdhui': taches.filter(
                statut__in=['EN_COURS', 'EN_ATTENTE'],
                dateEcheance=today
            ).count(),
            'demain': taches.filter(
                statut__in=['EN_COURS', 'EN_ATTENTE'],
                dateEcheance=demain
            ).count(),
            'en_retard': taches.filter(
                statut__in=['EN_COURS', 'EN_ATTENTE'],
                dateEcheance__lt=today
            ).count(),
        }
        return stats
# views.py
class PriorisationView(TemplateView):
    template_name = "base_tailwind/priorisation.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Récupérer le projet depuis l'URL
        projet_id = self.kwargs.get('projet_id')
        projet = get_object_or_404(Project, id=projet_id)
        context['projet'] = projet
        
        # Filtrer uniquement les tâches du projet non terminées
        taches = Taches.objects.filter(projet=projet).exclude(statut='TERMINE')
        today = date.today()
        
        # Calculer les dates de référence
        demain = today + timedelta(days=1)
        dans_3_jours = today + timedelta(days=3)
        dans_7_jours = today + timedelta(days=7)
        
        # Trier par urgence
        taches_triees = self._trier_par_urgence_reelle(taches, today)
        
        # Calculer les métriques
        metriques = self._calculer_metriques(taches_triees, today)
        
        context.update({
            'taches': taches_triees,
            'today': today,
            'demain': demain,
            'dans_3_jours': dans_3_jours,
            'dans_7_jours': dans_7_jours,
            'metriques': metriques,
        })
        return context

     
    
    def _trier_par_urgence_reelle(self, taches, today):
        """Trie les tâches par urgence réelle (retard > aujourd'hui > demain > etc.)"""
        
        def get_categorie_urgence(tache):
            jours_restants = (tache.dateEcheance - today).days
            
            if jours_restants < 0:
                return (1, abs(jours_restants))  # En retard : plus le retard est grand, plus c'est urgent
            elif jours_restants == 0:
                return (2, 0)  # Aujourd'hui
            elif jours_restants == 1:
                return (3, 0)  # Demain
            elif jours_restants <= 3:
                return (4, jours_restants)  # 2-3 jours
            elif jours_restants <= 7:
                return (5, jours_restants)  # 4-7 jours
            else:
                return (6, jours_restants)  # 8+ jours
        
        return sorted(taches, key=get_categorie_urgence)
    
    def _calculer_metriques(self, taches, today):
        """Calcul des métriques globales pour affichage - seulement tâches non terminées"""
        
        distribution = {
            'retard': 0, 
            'aujourdhui': 0, 
            'demain': 0,
            '3jours': 0,  # 2-3 jours
            'semaine': 0,  # 4-7 jours
            'lointain': 0  # 8+ jours
        }
        
        for tache in taches:
            jours = (tache.dateEcheance - today).days

            if jours < 0:
                distribution['retard'] += 1
            elif jours == 0:
                distribution['aujourdhui'] += 1
            elif jours == 1:
                distribution['demain'] += 1
            elif 2 <= jours <= 3:
                distribution['3jours'] += 1
            elif 4 <= jours <= 7:
                distribution['semaine'] += 1
            else:
                distribution['lointain'] += 1
        
        total = len(taches)
        if total > 0:
            taux_retard = distribution['retard'] * 100 / total
            charge_urgente = (distribution['retard'] + distribution['aujourdhui'] + distribution['demain']) * 100 / total
        else:
            taux_retard = 0
            charge_urgente = 0
        
        return {
            'distribution': distribution,
            'taux_retard': taux_retard,
            'charge_urgente': charge_urgente,
            'total_taches': total,
        }
def _calculer_metriques(self, taches, today):
    """Calcul des métriques globales pour affichage"""
    
    distribution = {
        'retard': 0, 
        '0j': 0, 
        '1j': 0,
        'j2_3': 0,  # Changé de '2-3j' à 'j2_3'
        'j4_7': 0,  # Changé de '4-7j' à 'j4_7'
        'j8_plus': 0  # Changé de '8+j' à 'j8_plus'
    }
    
    for tache in taches:
        jours = (tache.dateEcheance - today).days

        if jours < 0:
            distribution['retard'] += 1
        elif jours == 0:
            distribution['0j'] += 1
        elif jours == 1:
            distribution['1j'] += 1
        elif 2 <= jours <= 3:
            distribution['j2_3'] += 1
        elif 4 <= jours <= 7:
            distribution['j4_7'] += 1
        else:
            distribution['j8_plus'] += 1
    
    total = len(taches)
    if total > 0:
        taux_retard = distribution['retard'] * 100 / total
        charge_immediate = (distribution['0j'] + distribution['1j']) * 100 / total
    else:
        taux_retard = 0
        charge_immediate = 0
    
    return {
        'distribution': distribution,
        'taux_retard': taux_retard,
        'charge_immediate': charge_immediate,
    }
# Vue fonctionnelle pour marquer une tâche comme terminée
def terminer_tache(request, pk):
    tache = get_object_or_404(Taches, pk=pk)
    tache.statut = 'TERMINE'
    tache.resultat = 'SUCCES'
    tache.save()
    return redirect(reverse('Taches:project_taches', kwargs={'projet_id': tache.projet.id}))

