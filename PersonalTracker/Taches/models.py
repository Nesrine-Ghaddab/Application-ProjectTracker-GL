from django.db import models
from datetime import date
from Gestion_Projects.models import Project

class Taches(models.Model):
    idTache = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=255)
    description = models.TextField()
    dateEcheance = models.DateField()

    projet = models.ForeignKey(
    Project,
    on_delete=models.CASCADE,
    default=1,
    related_name="taches"
    )

    
    STATUT_CHOICES = [
        ('A_FAIRE', 'À faire'),
        ('EN_COURS', 'En cours'),
        ('TERMINE', 'Terminé'),
    ]
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='EN_COURS')

    RESULTAT_CHOICES = [
        ('SUCCES', 'Succès'),
        ('ECHEC', 'Échec'),
        ('INDETERMINE', 'Indéterminé'),
    ]
    resultat = models.CharField(max_length=12, choices=RESULTAT_CHOICES, default='INDETERMINE')

    def __str__(self):
        return f"{self.titre} - {self.statut} ({self.resultat})"

    def verifier_deadline(self):
        """Met à jour automatiquement le statut si la deadline est dépassée"""
        if self.dateEcheance < date.today() and self.statut != 'TERMINE':
            self.statut = 'TERMINE'
            self.resultat = 'ECHEC'
            self.save()

