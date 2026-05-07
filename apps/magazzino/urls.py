"""URLconf per l'applicazione `magazzino`.

Definisce le rotte per inventario, carico ricambio e alert scorte.
"""

from django.urls import path
from . import views

# Definiamo il namespace per l'app magazzino.
# Nel codice useremo {% url 'magazzino:inventario' %}
app_name = 'magazzino'

urlpatterns = [
    # Pagina principale del magazzino: mostra la lista di tutti i ricambi e le quantità.
    # URL: /magazzino/
    path('', views.inventario, name='inventario'),

    # Rotta dedicata al carico merci (es. quando arriva il corriere con i nuovi pezzi).
    # Punta alla vista che gestisce l'incremento delle scorte.
    # URL: /magazzino/carico/
    path('carico/', views.carico_ricambio, name='carico_ricambio'),

    # Pagina di utilità che filtra solo i ricambi la cui quantità è <= alla soglia minima.
    # Fondamentale per l'ufficio acquisti dell'officina.
    # URL: /magazzino/sotto-soglia/
    path('sotto-soglia/', views.alert_scorte, name='alert_scorte'),
]