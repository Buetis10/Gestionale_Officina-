from django.apps import AppConfig


class ClientiConfig(AppConfig):
    """
    Configurazione dell'applicazione clienti; serve a Django per registrare l'app e gestirne
    i dati-
    """
    # Specifica il tipo di campo da usare per le chiavi primarie (ID)
    # BigAutoField è lo standard moderno per gestire database di grandi dimensioni.
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.clienti' # fondamentale corrispondenza delle cartelle del progetto.
