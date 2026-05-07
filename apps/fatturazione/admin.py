"""Admin per il modulo `fatturazione`.

Personalizza la visualizzazione di `Fattura` e `Preventivo` nell'admin,
mostrando campi calcolati e collegamenti alle entità dell'officina.
"""

from django.contrib import admin
from .models import Fattura, Preventivo


@admin.register(Fattura)
class FatturaAdmin(admin.ModelAdmin):
    """
    Configurazione dell'interfaccia amministrativa per le Fatture.
    Gestisce la visualizzazione dei documenti emessi e dei totali calcolati.
    """
    
    # list_display: Definisce le colonne visibili nella tabella riassuntiva
    # 'get_targa' metodo per mostrare dati di altre app
    list_display = ('numero_documento', 'numero_progressivo', 'get_targa', 'tipo', 'data_emissione', 'totale_ivato', 'stato_pagamento')
    
    # list_filter: Aggiunge una colonna a destra per filtrare velocemente per tipologia o per data
    list_filter = ('tipo', 'data_emissione')
    
    # search_fields: Permette di cercare una fattura specifica tramite il suo numero o
    # risalendo alla targa del veicolo collegato all'ordine
    search_fields = ('numero_documento', 'ordine__veicolo__targa')
    
    # METODO GET_TARGA
    # Poichè la targa non è direttamente nel modello Fattura ma nell'Ordine, 
    # questo metodo salta tra i modelli per recuperare l'informazione
    def get_targa(self, obj):
        return obj.ordine.veicolo.targa
    
    # Titolo della colonna che apparirà nell'interfaccia Admin
    get_targa.short_description = 'Targa Veicolo'

    # readonly_fields: Impedisce la modifica manuale dei totali dall'admin.
    # Questi campi devono essere calcolati automaticamente dal sistema in base ai ricambi
    # e alla manodopera, per evitare discrepanze contabili umane.
    readonly_fields = ('totale_manodopera', 'totale_ricambi', 'totale_ivato')


@admin.register(Preventivo)
class PreventivoAdmin(admin.ModelAdmin):
    list_display = ('id', 'ordine', 'stato', 'data_creazione', 'totale_manodopera', 'totale_ricambi')
    list_filter = ('stato', 'data_creazione')
    search_fields = ('ordine__veicolo__targa',)
    readonly_fields = ('totale_manodopera', 'totale_ricambi')