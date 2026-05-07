from django.apps import AppConfig

class MagazzinoConfig(AppConfig):
    """
    Configurazione dell'applicazione 'magazzino'.
    Gestisce l'inventario, i carichi, gli scarichi e la logica delle scorte minime.
    """

    # Definisce il tipo di campo automatico per le chiavi primarie (ID).
    # BigAutoField garantisce che il database possa scalare senza problemi 
    # anche con un numero enorme di movimenti di magazzino.
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Nome univoco dell'applicazione nel progetto.
    # Specifica la posizione corretta all'interno della sottocartella 'apps'.
    name = 'apps.magazzino'