"""Admin per l'app `clienti`.

Qui definiamo come vengono visualizzati `Cliente` e `Veicolo` nell'interfaccia
di amministrazione di Django.
"""

from django.contrib import admin
from .models import Cliente, Veicolo


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'cognome', 'nome', 'telefono', 'email')
    search_fields = ('cognome', 'nome', 'codice_fiscale')


@admin.register(Veicolo)
class VeicoloAdmin(admin.ModelAdmin):
    list_display = ('targa', 'marca', 'modello', 'anno', 'km', 'cliente')
    search_fields = ('targa', 'marca', 'modello')
    list_filter = ('marca', 'anno')