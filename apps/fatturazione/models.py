from django.db import models
from apps.officina.models import OrdineLavoro
from apps.magazzino.models import MovimentoMagazzino
from decimal import Decimal
from django.db import transaction

class Fattura(models.Model):
    """
    MODELLO FATTURA: Gestisce la parte fiscale.
    Calcola automaticamente i totali leggendo i dati dalle altre app (Officina e Magazzino).
    """
    
    # Opzioni per i menu a tendina (Choices)
    TIPO_DOCUMENTO = [
        ('preventivo', 'Preventivo'),
        ('fattura', 'Fattura'),
    ]
    
    STATO_APPROVAZIONE = [
        ('bozza', 'In attesa'),
        ('approvato', 'Approvato'),
        ('rifiutato', 'Rifiutato'),
    ]

    # Relazione 1-a-1: un Ordine genera un solo documento fiscale.
    # Se elimini l'ordine, la fattura viene eliminata (CASCADE).
    ordine = models.OneToOneField(OrdineLavoro, on_delete=models.CASCADE, related_name='documento_fiscale')
    
    # Identificatori univoci
    numero_documento = models.CharField(max_length=40, unique=True, blank=True, null=True, help_text="Es: PREV-001 o FATT-001")
    numero_progressivo = models.PositiveIntegerField(blank=True, null=True, unique=True)
    data_emissione = models.DateField(auto_now_add=True) 
    
    tipo = models.CharField(max_length=20, choices=TIPO_DOCUMENTO, default='preventivo')
    stato = models.CharField(max_length=20, choices=STATO_APPROVAZIONE, default='bozza')
    
    # Campi monetari con DecimalField per evitare errori di precisione matematica
    totale_manodopera = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    totale_ricambi = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    iva_applicata = models.IntegerField(default=22) 
    totale_ivato = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    STATO_PAGAMENTO = [
        ('non_pagato', 'Non Pagato'),
        ('parziale', 'Parziale'),
        ('pagato', 'Pagato'),
    ]
    stato_pagamento = models.CharField(max_length=20, choices=STATO_PAGAMENTO, default='non_pagato')

    def calcola_totali(self):
        """
        LOGICA DI BUSINESS: 
        Aggrega i costi di manodopera e ricambi per calcolare il totale finale.
        """
        # 1. Recupera tutti gli interventi associati all'ordine e somma la manodopera
        interventi = self.ordine.interventi.all()
        self.totale_manodopera = sum(i.costo_manodopera for i in interventi)

        # 2. Recupera i pezzi di ricambio effettivamente usciti dal magazzino per questo ordine
        movimenti = MovimentoMagazzino.objects.filter(ordine_lavoro=self.ordine, tipo='uscita')
        self.totale_ricambi = sum(mov.quantita * mov.ricambio.prezzo_vendita for mov in movimenti)

        # 3. Calcolo dell'imponibile e aggiunta dell'IVA
        imponibile = Decimal(self.totale_manodopera) + Decimal(self.totale_ricambi)
        percentuale_iva = Decimal(self.iva_applicata) / Decimal(100)
        
        # Arrotondamento matematico corretto ai due decimali
        self.totale_ivato = (imponibile + (imponibile * percentuale_iva)).quantize(Decimal('0.01'))

    def save(self, *args, **kwargs):
        """
        Override del metodo save:
        Ogni volta che si salva, il sistema ricalcola i totali e gestisce la numerazione.
        """
        self.calcola_totali()
        
        # Se non c'è un numero progressivo, trova l'ultimo e incrementalo
        if not self.numero_progressivo:
            last = Fattura.objects.all().order_by('-numero_progressivo').first()
            next_num = 1 if not last or not last.numero_progressivo else last.numero_progressivo + 1
            self.numero_progressivo = next_num
            
        # Generazione automatica del numero documento leggibile (es: FATT-2024-0001)
        if not self.numero_documento:
            try:
                year = self.data_emissione.year
            except Exception:
                from datetime import date
                year = date.today().year
            self.numero_documento = f"FATT-{year}-{str(self.numero_progressivo).zfill(4)}"
        
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Fatture"

    def __str__(self):
        return f"{self.get_tipo_display()} n. {self.numero_documento} - {self.ordine.veicolo.targa}"


class Preventivo(models.Model):
    """
    MODELLO PREVENTIVO: Una versione 'pre-fiscale' del documento.
    """
    STATO = [
        ('bozza', 'Bozza'),
        ('approvato', 'Approvato'),
        ('rifiutato', 'Rifiutato'),
    ]

    ordine = models.OneToOneField(OrdineLavoro, on_delete=models.CASCADE, related_name='preventivo')
    data_creazione = models.DateTimeField(auto_now_add=True)
    stato = models.CharField(max_length=20, choices=STATO, default='bozza')
    totale_manodopera = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    totale_ricambi = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calcola(self):
        """Somma i costi senza calcolare l'IVA (per uso interno)."""
        interventi = self.ordine.interventi.all()
        self.totale_manodopera = sum(i.costo_manodopera for i in interventi)
        movimenti = MovimentoMagazzino.objects.filter(ordine_lavoro=self.ordine, tipo='uscita')
        self.totale_ricambi = sum(mov.quantita * mov.ricambio.prezzo_vendita for mov in movimenti)

    def salva_e_calcola(self):
        self.calcola()
        self.save()

    def genera_fattura(self, numero_documento=None, iva=22):
        """
        CONVERSIONE: Trasforma il preventivo approvato in una vera fattura.
        Usa una transazione atomica per garantire che l'operazione riesca completamente o fallisca del tutto.
        """
        if self.stato != 'approvato':
            raise ValueError('Il preventivo deve essere approvato per generare la fattura')

        with transaction.atomic():
            fattura = Fattura.objects.create(
                ordine=self.ordine,
                numero_documento=numero_documento or None,
                tipo='fattura',
                stato='approvato',
                totale_manodopera=self.totale_manodopera,
                totale_ricambi=self.totale_ricambi,
                iva_applicata=iva,
            )
            fattura.save()
            return fattura

    class Meta:
        verbose_name = "Preventivo"
        verbose_name_plural = "Preventivi"

    def __str__(self):
        return f"Preventivo #{self.id} - Ordine {self.ordine.id} - {self.get_stato_display()}"