"""URLconf per il modulo `fatturazione`.

Contiene le rotte per creare e visualizzare preventivi/fatture, inviarli via
email e generare il PDF stampabile.
"""

from django.urls import path
from . import views

# app_name fornisce un "cognome" agli URL di questa app.
# Nei template useremo: {% url 'fatturazione:genera_pdf_fattura' fattura.id %}
app_name = 'fatturazione'

urlpatterns = [
    # Visualizza lo storico o l'elenco di tutti i preventivi emessi.
    # URL: /fatturazione/preventivi/
    path('preventivi/', views.lista_preventivi, name='lista_preventivi'),

    # Crea un documento fiscale partendo da un ordine di lavoro specifico.
    # Il parametro <int:ordine_id> serve a legare la fattura al veicolo e ai lavori corretti.
    # URL: /fatturazione/crea-fattura/5/
    path('crea-fattura/<int:ordine_id>/', views.crea_fattura, name='crea_fattura'),

    # Questa è la rotta che abbiamo collegato al tasto rosso "Stampa PDF".
    # Richiama la vista che riempie il template 'pdf_temp.html' con i dati del database.
    # URL: /fatturazione/pdf/12/
    path('pdf/<int:fattura_id>/', views.genera_pdf_fattura, name='genera_pdf_fattura'),
    path('invia-preventivo/<int:preventivo_id>/', views.invia_preventivo, name='invia_preventivo'),
    path('converti-preventivo/<int:preventivo_id>/', views.converti_preventivo, name='converti_preventivo'),
]