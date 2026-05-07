"""Modelli per l'app `clienti`.

Definiscono le entità `Cliente` e `Veicolo` con i rispettivi campi
e relazioni (uno-a-molti). I metodi `__str__` aiutano la visualizzazione
nell'admin e nei menu a tendina.
"""

from django.db import models


class Cliente(models.Model):
    """
    MODELLO CLIENTE: Rappresenta l'anagrafica principale.
    Ogni cliente può possedere uno o più veicoli.
    """
    
    # CharField si usa per testi brevi. max_length è obbligatorio.
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    
    # Usiamo CharField per il telefono per gestire prefissi o spazi (+39...)
    telefono = models.CharField(max_length=20)
    
    # EmailField controlla automaticamente che l'indirizzo sia scritto bene (es. nome@mail.it)
    # blank=True e null=True permettono di non inserire l'email se il cliente non la fornisce
    email = models.EmailField(blank=True, null=True)
    
    # unique=True impedisce di registrare due volte lo stesso codice fiscale nel database
    codice_fiscale = models.CharField(max_length=16, unique=True)

    class Meta:
        # Nomi leggibili nel pannello di amministrazione
        verbose_name = "Cliente"
        verbose_name_plural = "Clienti"

    def __str__(self):
        """Metodo stringa: definisce come appare il cliente nei menu a tendina (es: Rossi Mario)"""
        return f"{self.cognome} {self.nome}"


class Veicolo(models.Model):
    """
    MODELLO VEICOLO: Contiene i dati tecnici del mezzo.
    È collegato al Cliente tramite una chiave esterna (ForeignKey).
    """
    
    # ForeignKey: Crea il legame 'Uno-a-Molti'. 
    # on_delete=models.CASCADE significa: se elimino il cliente, elimino anche i suoi veicoli.
    # related_name='veicoli' ci permette di scrivere 'cliente.veicoli.all' per vedere tutte le sue auto.
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='veicoli')
    
    # La targa deve essere unica per non avere doppioni nel database
    targa = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=50)
    modello = models.CharField(max_length=50)
    
    # PositiveIntegerField accetta solo numeri da 0 in su (perfetto per anni e chilometri)
    anno = models.PositiveIntegerField()
    km = models.PositiveIntegerField(default=0) # Impostiamo 0 come valore iniziale

    class Meta:
        verbose_name = "Veicolo"
        verbose_name_plural = "Veicoli"

    def __str__(self):
        """Visualizzazione standard dell'auto (es: AA123BB - Fiat Panda)"""
        return f"{self.targa} - {self.marca} {self.modello}"