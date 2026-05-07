from django.apps import AppConfig

class UtentiConfig(AppConfig):
    """
    Configurazione dell'applicazione 'utenti'.
    Gestisce l'autenticazione, i profili dei meccanici e i permessi.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.utenti'
    
    def ready(self):
        """
        Metodo eseguito all'avvio di Django.
        Viene utilizzato per collegare i 'Signals' (Segnali) all'applicazione.
        """
        # Importiamo il file signals.py qui e non all'inizio del file
        # per evitare errori di "importazione circolare" durante l'avvio.
        import apps.utenti.signals