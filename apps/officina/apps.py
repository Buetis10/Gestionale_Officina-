from django.apps import AppConfig

class OfficinaConfig(AppConfig):
    """
    Configurazione dell'applicazione 'officina'.
    È il modulo centrale che coordina l'attività pratica sui veicoli.
    """

    # Imposta il tipo di campo per le chiavi primarie (ID).
    # Utilizziamo BigAutoField per garantire che il database possa scalare
    # senza limiti nel conteggio degli ordini di lavoro e degli interventi.
    default_auto_field = 'django.db.models.BigAutoField'
    
    # L'indirizzo completo dell'app. 
    # Questo permette a Django di mappare correttamente i modelli dell'officina
    # anche se sono raggruppati all'interno della cartella 'apps/'.
    name = 'apps.officina'