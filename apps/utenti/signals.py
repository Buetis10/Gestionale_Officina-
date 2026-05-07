"""Signals per l'app `utenti`.

Qui definiamo il comportamento automatico che crea e sincronizza
il `Profilo` associato a ogni istanza di `User` appena creata o aggiornata.
"""

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profilo


@receiver(post_save, sender=User)
def gestisci_profilo_utente(sender, instance, created, **kwargs):
    """
    LOGICA AUTOMATICA:
    instance: rappresenta l'oggetto User appena salvato.
    created: è un booleano (True se è un nuovo utente, False se è una modifica).
    """
    if created:
        # 1. CREAZIONE: Se l'utente è nuovo, creiamo il Profilo collegato.
        # Di default il ruolo sarà 'meccanico' come definito nel modello.
        Profilo.objects.create(user=instance)
    
    # 2. AGGIORNAMENTO: Assicuriamo che ogni volta che l'User viene salvato,
    # anche i dati del suo profilo siano sincronizzati correttamente.
    instance.profilo.save()