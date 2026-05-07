"""URLconf dell'app 'officina'.

Definisce le rotte locali (dashboard, dettaglio ordine, aggiunte di interventi
e ricambi) e stabilisce il namespace `officina` usato nei template.
"""

from django.urls import path
from . import views

# Namespace dell'applicazione. 
# Permette di richiamare gli URL nei template con: {% url 'officina:dettaglio_ordine' ordine.id %}
app_name = 'officina'

urlpatterns = [
    # Pagina principale dell'officina. 
    # Solitamente mostra l'elenco delle auto attualmente sui ponti o in attesa.
    # URL: /officina/
    path('', views.dashboard, name='dashboard'), 
    
    # Punto di ingresso per l'accettazione.
    # Gestisce il modulo di ricerca rapida che abbiamo visto nella dashboard dei clienti.
    # URL: /officina/cerca-targa/
    path('cerca-targa/', views.cerca_targa, name='cerca_targa'),
    
    # Vista di dettaglio della singola riparazione.
    # Il parametro <int:pk> è la chiave primaria dell'ordine di lavoro.
    # Qui il meccanico vedrà gli interventi da fare e le note interne.
    # URL: /officina/ordine/42/
    path('ordine/<int:pk>/', views.dettaglio_ordine, name='dettaglio_ordine'),
    path('ordine/<int:pk>/aggiungi-ricambio/', views.aggiungi_ricambio, name='aggiungi_ricambio'),
    path('ordine/<int:pk>/aggiungi-intervento/', views.aggiungi_intervento, name='aggiungi_intervento'),
    path('ricambio-usato/<int:pk>/rimuovi/', views.rimuovi_ricambio_usato, name='rimuovi_ricambio_usato'),
]