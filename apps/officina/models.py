from django.db import models
from apps.clienti.models import Veicolo  # Importiamo il modello Veicolo dall'altra app
from django.contrib.auth.models import User # Usiamo gli utenti di Django come Meccanici

class OrdineLavoro(models.Model):
    """
    LA SCHEDA LAVORO:
    Rappresenta l'ingresso di un veicolo in officina. 
    Contiene le informazioni generali e lo stato di avanzamento.
    """
    STATO_CHOICES = [
        ('attesa', 'In Attesa'),
        ('lavorazione', 'In Lavorazione'),
        ('completato', 'Completato'),
        ('consegnato', 'Consegnato'),
    ]
    
    # Relazione con il veicolo: un ordine appartiene a un solo veicolo.
    veicolo = models.ForeignKey(Veicolo, on_delete=models.CASCADE, related_name='ordini')
    
    # Relazione con il meccanico: usiamo gli utenti registrati nel sistema.
    # Se un meccanico venisse eliminato dal sistema, l'ordine rimane (null=True).
    meccanico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    data_apertura = models.DateTimeField(auto_now_add=True)
    data_chiusura = models.DateTimeField(null=True, blank=True)
    
    stato = models.CharField(max_length=20, choices=STATO_CHOICES, default='attesa')
    
    # Campo per comunicazioni tra ufficio e officina (es. "il cliente ha fretta")
    note_interne = models.TextField(blank=True)

    class Meta:
        verbose_name = "Ordine di Lavoro"
        verbose_name_plural = "Ordini di Lavoro"

    def __str__(self):
        return f"Ordine {self.id} - {self.veicolo.targa} ({self.stato})"

class Intervento(models.Model):
    """
    DETTAGLIO LAVORI:
    Ogni riga di intervento rappresenta un'operazione specifica (es. Cambio Olio).
    Molti interventi compongono un singolo Ordine di Lavoro.
    """
    # Colleghiamo l'intervento al suo ordine "padre".
    ordine = models.ForeignKey(OrdineLavoro, on_delete=models.CASCADE, related_name='interventi')
    
    descrizione = models.CharField(max_length=255) # Es: "Sostituzione pastiglie anteriori"
    
    # Ore e Costi: campi fondamentali per il calcolo automatico della fattura.
    ore_lavorate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    costo_manodopera = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        verbose_name = "Singolo Intervento"
        verbose_name_plural = "Dettaglio Interventi"