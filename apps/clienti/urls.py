from django.urls import path
from . import views

# app_name definisce il "namespace". 
# Ci permette di richiamare gli URL nei template scrivendo {% url 'clienti:lista_clienti' %}
# evitando conflitti se altre app hanno nomi simili.
app_name = 'clienti'

urlpatterns = [
    # Pagina principale dell'app: mostra l'elenco di tutti i clienti.
    # Corrisponde a: /clienti/
    path('', views.lista_clienti, name='lista_clienti'),

    # Pagina per registrare un nuovo cliente.
    # Corrisponde a: /clienti/nuovo/
    path('nuovo/', views.crea_cliente, name='crea_cliente'),
    path('<int:cliente_id>/veicolo/nuovo/', views.crea_veicolo, name='crea_veicolo'),
    path('veicolo/<int:pk>/modifica/', views.modifica_veicolo, name='modifica_veicolo'),

    # Dettaglio di un cliente specifico.
    # <int:pk> è un segnaposto che accetta un numero intero (l'ID del cliente).
    # Django lo passerà alla funzione views.dettaglio_cliente come argomento.
    # Corrisponde a: /clienti/1/, /clienti/2/, ecc.
    path('<int:pk>/', views.dettaglio_cliente, name='dettaglio_cliente'),

    # Scheda tecnica di un veicolo specifico.
    # Anche qui usiamo <int:pk> per identificare quale veicolo mostrare.
    # Corrisponde a: /clienti/veicolo/5/
    path('veicolo/<int:pk>/', views.dettaglio_veicolo, name='dettaglio_veicolo'),
]