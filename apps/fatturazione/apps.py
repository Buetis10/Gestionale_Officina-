from django.apps import AppConfig


class FatturazioneConfig(AppConfig):
    
    """
    Configurazione dell'applicazione 'fatturazione'.
    Questo file definisce i metadati dell'app all'interno del progetto Django.
    """
    
    # Specifica il tipo di campo da utilizzare per le chiavi primarie generate automaticamente.
    # BigAutoField è un intero a 64 bit (ideale per tabelle con moltissimi record).
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Il percorso completo del pacchetto dell'applicazione.
    # In questo caso, l'app si trova nella cartella 'apps' sotto il nome 'fatturazione'.
    name = 'apps.fatturazione'