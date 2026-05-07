"""Form per l'anagrafica `Cliente` e `Veicolo`.

Definisce i widget Bootstrap per un rendering coerente nei template.
Separare la logica del form dal modello aiuta nella personalizzazione del layout.
"""

from django import forms
from .models import Cliente, Veicolo


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('nome', 'cognome', 'telefono', 'email', 'codice_fiscale')
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cognome': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'codice_fiscale': forms.TextInput(attrs={'class': 'form-control'}),
        }


class VeicoloForm(forms.ModelForm):
    class Meta:
        model = Veicolo
        fields = ('cliente', 'targa', 'marca', 'modello', 'anno', 'km')
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'targa': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modello': forms.TextInput(attrs={'class': 'form-control'}),
            'anno': forms.NumberInput(attrs={'class': 'form-control'}),
            'km': forms.NumberInput(attrs={'class': 'form-control'}),
        }
