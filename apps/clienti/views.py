"""View per la gestione clienti e veicoli.

Contengono le funzionalità per elencare, creare e modificare clienti e veicoli,
oltre alla ricerca per targa e alla visualizzazione della 'cartella' del veicolo.
"""

# Import degli strumenti standard di Django per template, database e redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F 
from .models import Veicolo, Cliente
from .forms import ClienteForm, VeicoloForm

# Import di modelli da altre app del progetto (Officina e Magazzino)
from apps.officina.models import OrdineLavoro
from apps.magazzino.models import Ricambio 

# Strumenti per la sicurezza: controllo login e controllo ruoli personalizzato
from django.contrib.auth.decorators import login_required
from apps.utenti.utils import role_required

@login_required 
@role_required(['titolare','receptionist'])
def lista_clienti(request):
    """
    Dashboard principale: gestisce la lista clienti, la ricerca veicoli 
    e fornisce alert su ordini aperti e scorte di magazzino.
    """
    
    # Recupera l'eventuale targa inserita nella barra di ricerca
    query = request.GET.get('targa')
    veicolo = None
    ordini_veicolo = None
    
    # --- SEZIONE RIEPILOGO STATO OFFICINA ---
    # Recupera tutti gli ordini che non sono ancora stati chiusi
    ordini_aperti = OrdineLavoro.objects.filter(
        stato__in=['attesa', 'lavorazione']
    ).order_by('-data_apertura')
    
    # ALERT MAGAZZINO:
    # Filtra i ricambi la cui quantità è sotto la soglia minima impostata.
    # L'oggetto F permette di confrontare due campi dello stesso record direttamente nel database.
    alert_magazzino = Ricambio.objects.filter(
        quantita_disponibile__lte=F('soglia_minima')
    )

    # --- LOGICA DI RICERCA VELOCE ---
    if query:
        # Cerca il veicolo tramite targa (ricerca parziale icontains)
        veicolo = Veicolo.objects.filter(targa__icontains=query).first()
        if veicolo:
            # Se trovato, recupera tutta la cronologia interventi per quel veicolo
            ordini_veicolo = OrdineLavoro.objects.filter(veicolo=veicolo).order_by('-data_apertura')
    
    # Recupera la lista completa dei clienti ordinata alfabeticamente
    clienti = Cliente.objects.all().order_by('cognome', 'nome')
    
    return render(request, 'clienti/lista_clienti.html', {
        'clienti': clienti,
        'veicolo_trovato': veicolo, 
        'ordini': ordini_veicolo,
        'query': query,
        'ordini_aperti': ordini_aperti,
        'alert_magazzino': alert_magazzino,
    })

# ----------------------- GESTIONE ANAGRAFICA --------------------

@login_required
@role_required(['titolare','receptionist'])
def crea_cliente(request):
    """Gestisce la creazione di un nuovo cliente tramite form."""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            # Dopo il salvataggio, reindirizza alla scheda del cliente appena creato
            return redirect('clienti:dettaglio_cliente', pk=cliente.pk)
    else:
        form = ClienteForm()
    return render(request, 'clienti/form_cliente.html', {'form': form})

@login_required
@role_required(['titolare','receptionist'])
def dettaglio_cliente(request, pk):
    """Visualizza il profilo completo di un cliente e i veicoli associati."""
    cliente = get_object_or_404(Cliente, pk=pk)
    veicoli = cliente.veicoli.all() # Sfrutta la relation per elencare le auto del cliente
    return render(request, 'clienti/dettaglio_cliente.html', {'cliente': cliente, 'veicoli': veicoli})


@login_required
@role_required(['titolare','receptionist'])
def crea_veicolo(request, cliente_id=None):
    """Aggiunge un veicolo al database, opzionalmente pre-associandolo a un cliente."""
    if request.method == 'POST':
        form = VeicoloForm(request.POST)
        if form.is_valid():
            v = form.save()
            return redirect('clienti:dettaglio_cliente', pk=v.cliente.pk)
    else:
        # Se passiamo un cliente_id dall'URL, il form sarà già precompilato con quel cliente
        initial = {}
        if cliente_id:
            initial['cliente'] = cliente_id
        form = VeicoloForm(initial=initial)
    return render(request, 'clienti/form_veicolo.html', {'form': form})


@login_required
@role_required(['titolare','receptionist'])
def modifica_veicolo(request, pk):
    """Permette di modificare i dati (es. km, anno) di un veicolo esistente."""
    v = get_object_or_404(Veicolo, pk=pk)
    if request.method == 'POST':
        # Passiamo 'instance=v' per aggiornare il record esistente invece di crearne uno nuovo
        form = VeicoloForm(request.POST, instance=v)
        if form.is_valid():
            form.save()
            return redirect('clienti:dettaglio_cliente', pk=v.cliente.pk)
    else:
        form = VeicoloForm(instance=v)
    return render(request, 'clienti/form_veicolo.html', {'form': form, 'veicolo': v})

@login_required
@role_required(['titolare','receptionist','meccanico'])
def dettaglio_veicolo(request, pk):
    """
    Mostra la 'cartella clinica' del veicolo.
    Accessibile anche ai meccanici, ma con restrizioni di privacy.
    """
    veicolo = get_object_or_404(Veicolo, pk=pk)
    
    # Recupera lo storico completo degli interventi
    storico = OrdineLavoro.objects.filter(veicolo=veicolo).order_by('-data_apertura')
    
    # LOGICA DI SICUREZZA PER IL MECCANICO:
    # Un meccanico può vedere i dettagli del veicolo solo se vi ha effettivamente lavorato.
    if hasattr(request.user, 'profilo') and request.user.profilo.ruolo == 'meccanico':
        ha_accesso = OrdineLavoro.objects.filter(veicolo=veicolo, meccanico=request.user).exists()
        if not ha_accesso:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden('Accesso negato: non sei assegnato a questo veicolo.')

    return render(request, 'clienti/dettaglio_veicolo.html', {
        'veicolo': veicolo,
        'ordini': storico
    })