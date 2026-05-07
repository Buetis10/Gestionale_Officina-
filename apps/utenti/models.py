"""Modello `Profilo` per estendere l'utente Django.

Contiene il ruolo dell'utente e informazioni di contatto usate
dalle view e dal sistema di autorizzazione basato sui ruoli.
"""

from django.db import models
from django.contrib.auth.models import User


class Profilo(models.Model):
    """
    ESTENSIONE UTENTE:
    Django fornisce già gestione di password e username. Questo modello aggiunge
    le informazioni specifiche necessarie all'officina.
    """
    RUOLI = [
        ('titolare', 'Titolare'),
        ('meccanico', 'Meccanico'),
        ('receptionist', 'Receptionist'),
    ]
    
    # Relazione OneToOne: ogni utente ha un solo profilo e viceversa.
    # on_delete=models.CASCADE: se elimini l'utente, il suo profilo viene rimosso.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profilo')
    
    # Definisce cosa può fare l'utente nel sistema.
    ruolo = models.CharField(max_length=20, choices=RUOLI, default='meccanico')
    
    # Informazioni di contatto aggiuntive
    telefono = models.CharField(max_length=15, blank=True)

    def __str__(self):
        """Esempio: 'mario.rossi - Meccanico'"""
        return f"{self.user.username} - {self.get_ruolo_display()}"