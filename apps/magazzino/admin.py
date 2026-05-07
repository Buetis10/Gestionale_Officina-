"""Configurazioni Admin per l'app `magazzino`.

Contiene le classi che personalizzano l'interfaccia di amministrazione
per `Ricambio`, `MovimentoMagazzino` e `RicambioUsato`.
"""

from django.contrib import admin
from .models import Ricambio, MovimentoMagazzino
from .models import RicambioUsato
from django.utils.html import format_html

@admin.register(Ricambio)
class RicambioAdmin(admin.ModelAdmin):
    """
    Configurazione dell'interfaccia Admin per l'anagrafica Ricambi.
    Permette di monitorare le scorte e i prezzi di vendita.
    """
    # Colonne visibili nella tabella principale del magazzino.
    list_display = ('codice', 'descrizione', 'quantita_disponibile', 'soglia_minima', 'prezzo_vendita')
    
    # list_editable: Permette di modificare la soglia minima direttamente dalla lista 
    # senza aprire il dettaglio del ricambio. Velocizza la gestione degli alert scorte.
    list_editable = ('soglia_minima',) 
    
    # Ricerca rapida per codice articolo (es. codice a barre) o descrizione prodotto.
    search_fields = ('codice', 'descrizione')

@admin.register(MovimentoMagazzino)
class MovimentoAdmin(admin.ModelAdmin):
    """
    Configurazione per il registro dei Movimenti.
    Tiene traccia di ogni pezzo che entra o esce dall'officina.
    """
    # Mostra quale ricambio è stato mosso, se è un'entrata (acquisto) o uscita (riparazione).
    # Mostra anche l'ordine di lavoro collegato per sapere su quale auto è finito il pezzo.
    list_display = ('ricambio', 'tipo', 'quantita', 'data', 'ordine_lavoro')
    
    # Filtri laterali: Permettono di vedere, ad esempio, tutti i movimenti di oggi 
    # o solo le uscite verso l'officina.
    list_filter = ('tipo', 'data')


@admin.register(RicambioUsato)
class RicambioUsatoAdmin(admin.ModelAdmin):
    list_display = ('ricambio', 'ordine_lavoro', 'intervento', 'quantita', 'prezzo_unitario', 'data')
    search_fields = ('ricambio__codice', 'ordine_lavoro__id', 'intervento__descrizione')
    readonly_fields = ('preview',)

    def preview(self, obj):
        return format_html('<strong>{}</strong> x{}', obj.ricambio.codice, obj.quantita)
    preview.short_description = 'Anteprima'