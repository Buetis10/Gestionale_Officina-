"""View per la fatturazione: preventivi e fatture.

Contiene le view protette da ruolo `titolare` per creare, inviare e
generare PDF dei documenti fiscali.
"""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Fattura 
from .models import Preventivo
from .forms import PreventivoForm
from django.shortcuts import redirect
from apps.officina.models import OrdineLavoro
from apps.utenti.utils import role_required

# Prova a importare WeasyPrint per la generazione dei PDF.
# Se non è installato nel sistema, imposta HTML a None per evitare il crash del server.
try:
    from weasyprint import HTML
except Exception:
    HTML = None


@login_required
@role_required(['titolare'])
def lista_preventivi(request):
    """
    Recupera tutti i preventivi dal database.
    Usa select_related per ottimizzare la query, recuperando anche veicolo e ordine 
    in un colpo solo (evita il problema delle query N+1).
    """
    preventivi = Preventivo.objects.select_related('ordine__veicolo').all().order_by('-data_creazione')
    return render(request, 'fatturazione/lista_preventivi.html', {'preventivi': preventivi})

@login_required
@role_required(['titolare'])
def crea_fattura(request, ordine_id):
    """
    Crea o recupera un preventivo associato a un Ordine di Lavoro specifico.
    """
    ordine = get_object_or_404(OrdineLavoro, pk=ordine_id)
    
    # get_or_create: se non esiste un preventivo per questo ordine, lo crea sul momento.
    preventivo, created = Preventivo.objects.get_or_create(ordine=ordine)

    if request.method == 'POST':
        # Carica il form con i dati inviati e l'istanza del preventivo esistente
        form = PreventivoForm(request.POST, instance=preventivo)
        if form.is_valid():
            form.save()
            # Metodo del modello che somma i costi di ricambi e manodopera
            preventivo.salva_e_calcola()
            return redirect('fatturazione:lista_preventivi')
    else:
        form = PreventivoForm(instance=preventivo)

    return render(request, 'fatturazione/form_fattura.html', {'form': form, 'ordine': ordine, 'preventivo': preventivo})

@login_required
@role_required(['titolare'])
def genera_pdf_fattura(request, fattura_id):
    """
    Prepara la visualizzazione della fattura per la stampa o generazione PDF.
    """
    # Recupera la fattura o restituisce 404 se l'ID è inesistente
    fattura = get_object_or_404(Fattura, id=fattura_id)
    return render(request, 'fatturazione/pdf_temp.html', {'fattura': fattura})


@login_required
@role_required(['titolare','receptionist'])
def invia_preventivo(request, preventivo_id):
    """
    Logica complessa: genera un PDF in memoria, lo allega a una mail
    e lo spedisce all'indirizzo del cliente.
    """
    from django.core.mail import EmailMessage
    from django.template.loader import render_to_string
    from django.conf import settings
    
    preventivo = get_object_or_404(Preventivo, id=preventivo_id)
    cliente = preventivo.ordine.veicolo.cliente
    
    # Controllo di sicurezza: se il cliente non ha email, ferma la procedura
    if not cliente.email:
        return render(request, 'fatturazione/errore_email.html', {'message': 'Il cliente non ha un indirizzo email.'})

    # Trasforma il template HTML del preventivo in una stringa di testo
    html_string = render_to_string('fatturazione/pdf_preventivo.html', {'preventivo': preventivo})
    
    # Se WeasyPrint è disponibile, genera il file binario PDF
    if HTML:
        pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()
    else:
        pdf = None

    # Configurazione dell'oggetto Email
    subject = f'Preventivo Officina - Ordine #{preventivo.ordine.id}'
    body = f'Gentile {cliente.nome} {cliente.cognome},\n\nIn allegato trova il preventivo per il lavoro richiesto.\n\nCordiali saluti.'
    
    email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [cliente.email])
    
    # Se il PDF è stato generato con successo, lo allega alla mail
    if pdf:
        email.attach(f'Preventivo_Ordine_{preventivo.ordine.id}.pdf', pdf, 'application/pdf')
    
    # Invio della mail (fail_silently=False genera un errore se l'invio fallisce)
    email.send(fail_silently=False)
    
    return render(request, 'fatturazione/inviato.html', {'cliente': cliente, 'preventivo': preventivo})


@login_required
@role_required(['titolare'])
def converti_preventivo(request, preventivo_id):
    """
    Passaggio finale: trasforma ufficialmente il preventivo (proposta) 
    in fattura (documento fiscale emesso).
    """
    preventivo = get_object_or_404(Preventivo, id=preventivo_id)
    
    # Impedisce la fatturazione se il cliente non ha ancora dato l'approvazione formale
    if preventivo.stato != 'approvato':
        return render(request, 'fatturazione/errore_email.html', {'message': 'Il preventivo non è approvato.'})

    # Chiama il metodo del modello Preventivo che crea un record Fattura e copia i dati
    fattura = preventivo.genera_fattura()
    
    # Reindirizza l'utente alla visualizzazione della fattura appena creata
    return redirect('fatturazione:genera_pdf_fattura', fattura_id=fattura.id)