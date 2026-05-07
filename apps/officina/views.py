"""View dell'app `officina`.

Contengono le view principali per la dashboard, la ricerca targa,
la gestione degli ordini di lavoro, interventi e ricambi usati.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.utenti.utils import role_required
from django.db.models import F
from django.http import HttpResponse                  
from django.template.loader import render_to_string   

# Import dei modelli cross-app (il cuore dell'integrazione del sistema)
from apps.officina.models import OrdineLavoro
from apps.clienti.models import Veicolo
from apps.magazzino.models import Ricambio
from apps.fatturazione.models import Fattura 
from apps.magazzino.models import RicambioUsato
from django import forms
from apps.officina.models import Intervento

# Gestione robusta della libreria PDF: se WeasyPrint non è installato, il sistema non crasha
try:
    from weasyprint import HTML
except ImportError:
    HTML = None

@login_required
@role_required(['titolare','receptionist','meccanico'])
def dashboard(request):
    """
    PANNELLO DI CONTROLLO PRINCIPALE:
    Fornisce una panoramica dello stato dell'officina.
    """
    # 1. Statistiche rapide per i badge informativi in alto nella pagina
    in_attesa = OrdineLavoro.objects.filter(stato='attesa').count()
    in_lavorazione = OrdineLavoro.objects.filter(stato='lavorazione').count()
    completati = OrdineLavoro.objects.filter(stato='completato').count()
    
    # 2. Alert scorte: identifica i ricambi sotto la soglia minima per l'acquisto
    alert_magazzino = Ricambio.objects.filter(quantita_disponibile__lt=F('soglia_minima'))
    
    # 3. Logica di filtraggio per ruolo:
    # Il Meccanico vede solo i suoi lavori; Titolare e Receptionist vedono tutto.
    ordini_aperti = []
    if hasattr(request.user, 'profilo') and request.user.profilo.ruolo:
        ruolo_attuale = request.user.profilo.ruolo.lower().strip()
        
        if ruolo_attuale == 'meccanico':
            ordini_aperti = OrdineLavoro.objects.filter(meccanico=request.user).order_by('-data_apertura')
            # Fallback se non ci sono ordini assegnati per evitare una dashboard vuota
            if not ordini_aperti.exists():
                ordini_aperti = OrdineLavoro.objects.filter(stato__in=['attesa','lavorazione']).order_by('-data_apertura')
        else:
            # Visualizzazione limitata agli ultimi 10 per Titolare/Receptionist (performance)
            ordini_aperti = OrdineLavoro.objects.all().order_by('-data_apertura')[:10]
    else:
        ordini_aperti = OrdineLavoro.objects.all().order_by('-data_apertura')[:10]

    context = {
        'in_attesa': in_attesa,
        'in_lavorazione': in_lavorazione,
        'completati': completati,
        'alert_magazzino': alert_magazzino,
        'ordini_aperti': ordini_aperti,
    }
    return render(request, 'dashboard.html', context)

@login_required
@role_required(['titolare','receptionist','meccanico'])
def cerca_targa(request):
    """Motore di ricerca: trova un veicolo per targa e reindirizza all'ultimo ordine aperto."""
    query = request.GET.get('q', '').strip().upper()
    if query:
        veicolo = Veicolo.objects.filter(targa__icontains=query).first()
        if veicolo:
            ultimo_ordine = OrdineLavoro.objects.filter(veicolo=veicolo).order_by('-data_apertura').first()
            if ultimo_ordine:
                return redirect('officina:dettaglio_ordine', pk=ultimo_ordine.pk)
            else:
                return redirect('clienti:dettaglio_veicolo', pk=veicolo.pk)
    return redirect('officina:dashboard')

@login_required
@role_required(['titolare','receptionist','meccanico'])
def dettaglio_ordine(request, pk):
    """
    SCHEDA TECNICA: Visualizza tutti i dettagli di un ordine specifico.
    Include controllo accessi per evitare che i meccanici vedano ordini non assegnati.
    """
    ordine = get_object_or_404(OrdineLavoro, pk=pk)
    ruolo = getattr(getattr(request.user, 'profilo', None), 'ruolo', None)
    ricambi = Ricambio.objects.all()
    
    if ruolo == 'meccanico' and ordine.meccanico != request.user:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden('Accesso negato: ordine non assegnato')
        
    return render(request, 'officina/dettaglio_ordine.html', {'ordine': ordine, 'ricambi': ricambi})

@login_required
@role_required('titolare')
def genera_pdf_fattura(request, fattura_id):
    """
    GENERAZIONE PDF: Trasforma la fattura in formato PDF e chiude l'ordine di lavoro.
    Utilizza WeasyPrint per il rendering dell'HTML.
    """
    fattura = get_object_or_404(Fattura, id=fattura_id)
    ordine = fattura.ordine 
    
    # Automatismo: se stampi la fattura, il lavoro è considerato completato
    if ordine.stato != 'completato':
        ordine.stato = 'completato'
        ordine.save()

    if HTML:
        # Rendering del template HTML dedicato alla stampa
        html_string = render_to_string('fatturazione/pdf_temp.html', {'fattura': fattura})
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        result = html.write_pdf()

        # Risposta HTTP con file PDF invece di una pagina web
        response = HttpResponse(result, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="Fattura_{ordine.veicolo.targa}.pdf"'
        return response
    else:
        return HttpResponse("Errore: WeasyPrint non configurato correttamente.")

@login_required
@role_required(['titolare','receptionist','meccanico'])
def aggiungi_ricambio(request, pk):
    """Aggiunge un pezzo di ricambio all'ordine di lavoro corrente."""
    ordine = get_object_or_404(OrdineLavoro, pk=pk)

    # Form interno veloce per la selezione ricambio e quantità
    class _Form(forms.Form):
        ricambio = forms.ModelChoiceField(queryset=Ricambio.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
        quantita = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    if request.method == 'POST':
        form = _Form(request.POST)
        if form.is_valid():
            ricambio = form.cleaned_data['ricambio']
            quantita = form.cleaned_data['quantita']
            # Registra l'uso del ricambio (questo attiverà lo scarico magazzino tramite i segnali del modello)
            ru = RicambioUsato.objects.create(
                ricambio=ricambio,
                ordine_lavoro=ordine,
                quantita=quantita,
                prezzo_unitario=ricambio.prezzo_vendita,
            )
            return redirect('officina:dettaglio_ordine', pk=ordine.pk)
    else:
        form = _Form()

    return render(request, 'officina/aggiungi_ricambio.html', {'form': form, 'ordine': ordine})

@login_required
@role_required(['titolare','meccanico'])
def aggiungi_intervento(request, pk):
    """Registra la manodopera (tempo e costo) per l'ordine di lavoro."""
    ordine = get_object_or_404(OrdineLavoro, pk=pk)

    class _Form(forms.ModelForm):
        class Meta:
            model = Intervento
            fields = ('descrizione', 'ore_lavorate', 'costo_manodopera')
            widgets = {
                'descrizione': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
                'ore_lavorate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.25'}),
                'costo_manodopera': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            }

    if request.method == 'POST':
        form = _Form(request.POST)
        if form.is_valid():
            interv = form.save(commit=False)
            interv.ordine = ordine
            interv.save()
            return redirect('officina:dettaglio_ordine', pk=ordine.pk)
    else:
        form = _Form()
    return render(request, 'officina/aggiungi_intervento.html', {'form': form, 'ordine': ordine})

@login_required
@role_required(['titolare', 'receptionist', 'meccanico'])
def rimuovi_ricambio_usato(request, pk):
    """
    Rimuove un ricambio precedentemente aggiunto a un ordine di lavoro.
    Il sistema di Django gestirà automaticamente il ripristino delle scorte 
    se hai impostato i segnali (signals) nel modello RicambioUsato.
    """
    ricambio_usato = get_object_or_404(RicambioUsato, pk=pk)
    ordine_id = ricambio_usato.ordine_lavoro.pk
    
    if request.method == 'POST':
        ricambio_usato.delete()
        return redirect('officina:dettaglio_ordine', pk=ordine_id)
    
    return render(request, 'officina/conferma_elimina_ricambio.html', {
        'ricambio': ricambio_usato
    })