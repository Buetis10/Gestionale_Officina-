from django.db import models, transaction
from apps.officina.models import OrdineLavoro, Intervento

class Ricambio(models.Model):
    """
    ANAGRAFICA RICAMBI:
    Rappresenta l'oggetto fisico presente in magazzino.
    """
    codice = models.CharField(max_length=50, unique=True) # Codice SKU o codice a barre
    descrizione = models.CharField(max_length=255)
    categoria = models.CharField(max_length=100, blank=True)
    
    # Stato scorte
    quantita_disponibile = models.IntegerField(default=0)
    soglia_minima = models.IntegerField(default=5) # Trigger per l'alert nella dashboard
    
    # Dati economici per il calcolo dei margini e delle fatture
    prezzo_acquisto = models.DecimalField(max_digits=10, decimal_places=2)
    prezzo_vendita = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "Ricambi"

    def __str__(self):
        return f"{self.codice} - {self.descrizione} ({self.quantita_disponibile} pz)"

class MovimentoMagazzino(models.Model):
    """
    LOGICA DEI MOVIMENTI:
    Ogni riga di questa tabella modifica automaticamente la 'quantita_disponibile' nel modello Ricambio.
    """
    TIPO_MOVIMENTO = [
        ('entrata', 'Entrata (Rifornimento)'),
        ('uscita', 'Uscita (Riparazione)'),
    ]
    
    ricambio = models.ForeignKey(Ricambio, on_delete=models.CASCADE, related_name='movimenti')
    # Se un ordine viene cancellato, manteniamo il movimento (null=True) per scopi di inventario storico
    ordine_lavoro = models.ForeignKey(OrdineLavoro, on_delete=models.SET_NULL, null=True, blank=True)
    
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMENTO)
    quantita = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Garantisce che il magazzino si aggiorni correttamente ad ogni salvataggio.
        """
        # 'transaction.atomic' assicura che se il salvataggio del movimento fallisce, 
        # le scorte del ricambio non vengano modificate (operazione tutto-o-niente).
        with transaction.atomic():
            # CASO MODIFICA: Se il movimento esiste già, storniamo il vecchio valore prima di applicare il nuovo
            if self.pk:
                vecchio_movimento = MovimentoMagazzino.objects.get(pk=self.pk)
                if vecchio_movimento.tipo == 'entrata':
                    self.ricambio.quantita_disponibile -= vecchio_movimento.quantita
                else:
                    self.ricambio.quantita_disponibile += vecchio_movimento.quantita

            # APPLICAZIONE MOVIMENTO: Aggiorniamo il totale nel magazzino
            if self.tipo == 'entrata':
                self.ricambio.quantita_disponibile += self.quantita
            else:
                self.ricambio.quantita_disponibile -= self.quantita
            
            # Salvataggio sincronizzato
            self.ricambio.save()
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Se un movimento viene eliminato, le scorte vengono ripristinate (es. annullo uno scarico).
        """
        with transaction.atomic():
            if self.tipo == 'entrata':
                self.ricambio.quantita_disponibile -= self.quantita
            else:
                self.ricambio.quantita_disponibile += self.quantita
            self.ricambio.save()
            super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Movimenti Magazzino"


class RicambioUsato(models.Model):
    """
    Collega un `Ricambio` a un `Intervento` o a un `OrdineLavoro` indicando
    la quantità utilizzata e il prezzo unitario. Alla creazione viene
    generato un `MovimentoMagazzino` di tipo 'uscita' per aggiornare le scorte.
    """
    ricambio = models.ForeignKey(Ricambio, on_delete=models.CASCADE, related_name='usi')
    intervento = models.ForeignKey(Intervento, on_delete=models.SET_NULL, null=True, blank=True, related_name='ricambi_usati')
    ordine_lavoro = models.ForeignKey(OrdineLavoro, on_delete=models.CASCADE, related_name='ricambi_usati')
    quantita = models.PositiveIntegerField(default=1)
    prezzo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)
    movimento = models.OneToOneField(MovimentoMagazzino, on_delete=models.SET_NULL, null=True, blank=True, related_name='ricambio_collegato')

    def save(self, *args, **kwargs):
        # Gestione creazione e aggiornamento:
        is_new = self.pk is None
        old_quantita = None
        if not is_new:
            try:
                old = RicambioUsato.objects.get(pk=self.pk)
                old_quantita = old.quantita
            except RicambioUsato.DoesNotExist:
                old_quantita = None

        super().save(*args, **kwargs)

        if is_new:
            mov = MovimentoMagazzino.objects.create(
                ricambio=self.ricambio,
                ordine_lavoro=self.ordine_lavoro,
                tipo='uscita',
                quantita=self.quantita,
            )
            # colleghiamo il movimento creato a questo record
            self.movimento = mov
            super().save(update_fields=['movimento'])
        else:
            # Se la quantità è cambiata ed esiste un movimento collegato, aggiorniamolo
            if self.movimento and old_quantita is not None and self.quantita != old_quantita:
                mov = self.movimento
                mov.quantita = self.quantita
                mov.save()

    def delete(self, *args, **kwargs):
        # Se esiste il movimento collegato, eliminiamolo (questo ripristina la giacenza)
        if self.movimento:
            try:
                self.movimento.delete()
            except MovimentoMagazzino.DoesNotExist:
                pass
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.ricambio.codice} x{self.quantita} per Ordine {self.ordine_lavoro.id}"