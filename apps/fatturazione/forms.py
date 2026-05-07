"""Form per gestione di Preventivi/Fatture.

Contiene i widget e le configurazioni utili per il rendering dei campi
nel template. È separato dal modello per poter personalizzare il layout
senza toccare la logica del modello.
"""

from django import forms
from .models import Preventivo


class PreventivoForm(forms.ModelForm):
    """
    Classe ModelForm per l'entità Preventivo.
    Semplifica il processo di creazione e validazione dei dati legati al modello.
    """
    class Meta:
        # Indica a Django quale modello deve essere usato per generare il form
        model = Preventivo
        
        # Specifica quali campi del modello devono essere inclusi nel form
        # In questo caso, viene esposto solo il campo 'stato'
        fields = ('stato',)
        
        # Personalizzazione dei widget (gli elementi HTML del form)
        widgets = {
            # Associa al campo 'stato' un menu a tendina (Select) 
            # e aggiunge la classe CSS Bootstrap 'form-select' per lo styling
            'stato': forms.Select(attrs={'class': 'form-select'})
        }