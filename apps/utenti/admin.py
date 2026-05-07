"""Admin per l'app `utenti`.

Definisce come visualizzare i profili utente nell'interfaccia di amministrazione.
"""

from django.contrib import admin
from .models import Profilo  


@admin.register(Profilo)
class ProfiloAdmin(admin.ModelAdmin):
    list_display = ('user', 'ruolo')  # Mostra l'utente e il suo ruolo nella lista
