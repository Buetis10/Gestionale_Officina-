"""View per il modulo `magazzino`.

Contengono le view per visualizzare l'inventario, registrare carichi e
segnalare scorte basse. Le view richiedono permessi adeguati (titolare/receptionist).
"""

# Importazioni standard di Django per il rendering e la sicurezza
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.utenti.utils import role_required

# F permette di eseguire query che confrontano campi diversi dello stesso modello nel DB
from django.db.models import F
from .models import Ricambio

@login_required
@role_required(['titolare','receptionist'])
def inventario(request):
    """
    VISUALIZZAZIONE MAGAZZINO:
    Recupera l'elenco completo dei ricambi presenti nel database.
    Passa i dati al template per costruire la tabella dell'inventario.
    """
    # Query set che estrae tutti gli oggetti Ricambio senza filtri
    ricambi = Ricambio.objects.all()
    return render(request, 'magazzino/inventario.html', {'ricambi': ricambi})

@login_required
@role_required(['titolare','receptionist'])
def carico_ricambio(request):
    """
    GESTIONE ENTRATE:
    Richiama il modulo (form) per registrare l'arrivo di nuovi pezzi.
    La logica di aggiornamento scorte è gestita dal metodo save() nel modello.
    """
    # Carica semplicemente il template del form; la logica POST sarà gestita altrove o tramite ModelForm
    return render(request, 'magazzino/form_carico.html')

@login_required
@role_required(['titolare','receptionist'])
def alert_scorte(request):
    """
    LOGICA DI APPROVIGIONAMENTO:
    Filtra i ricambi la cui quantità disponibile è strettamente inferiore 
    alla soglia minima impostata.
    
    L'uso di F('soglia_minima') permette di confrontare due campi 
    dello stesso record direttamente nel database (efficiente a livello di performance).
    """
    # Filtra i record dove quantita_disponibile < soglia_minima
    scarsi = Ricambio.objects.filter(quantita_disponibile__lt=F('soglia_minima'))
    return render(request, 'magazzino/alert.html', {'ricambi': scarsi})