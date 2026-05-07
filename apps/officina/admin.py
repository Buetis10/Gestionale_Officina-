"""Amministrazione Django per l'app `officina`.

Qui definiamo gli inline e le personalizzazioni dell'admin per visualizzare
e modificare gli `OrdineLavoro` e i relativi `Intervento` direttamente dalla
dashboard di amministrazione di Django.
"""

from django.contrib import admin
from .models import OrdineLavoro, Intervento


# CONFIGURAZIONE INLINE:
# Questa classe permette di inserire gli interventi "dentro" la pagina dell'ordine di lavoro.
# Invece di salvare l'ordine e poi andare nella sezione Interventi, fai tutto insieme.
class InterventoInline(admin.TabularInline):
    model = Intervento
    # extra = 1: Mostra una riga vuota aggiuntiva in fondo alla lista degli interventi,
    # pronta per essere compilata con un nuovo lavoro.
    extra = 1 


@admin.register(OrdineLavoro)
class OrdineLavoroAdmin(admin.ModelAdmin):
    """
    Gestione delle Schede Lavoro (Ordini).
    È il pannello di controllo per monitorare cosa stanno facendo i meccanici.
    """
    # Visualizzazione rapida: ID ordine, targa veicolo, stato (attesa/lavorazione/chiuso) e chi ci lavora.
    list_display = ('id', 'veicolo', 'stato', 'data_apertura', 'meccanico')
    
    # Filtri: Utili per vedere solo le auto "In lavorazione" o i lavori assegnati a un certo meccanico.
    list_filter = ('stato', 'meccanico')
    
    # L'arma segreta: Inserendo InterventoInline, la pagina dell'ordine mostrerà 
    # una tabella in basso con tutti i lavori eseguiti su quel veicolo in quell'occasione.
    inlines = [InterventoInline]