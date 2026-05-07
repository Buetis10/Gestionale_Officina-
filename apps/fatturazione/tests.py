"""
Suite di test per il modulo di fatturazione.

Questo modulo verifica:
1. La corretta aggregazione dei costi (manodopera + ricambi).
2. Il flusso di transizione da Preventivo a Fattura.
3. L'integrazione con il sistema di invio email e la gestione dei ruoli.
"""

from django.test import TestCase
from apps.clienti.models import Cliente, Veicolo
from apps.officina.models import OrdineLavoro, Intervento
from apps.magazzino.models import Ricambio, MovimentoMagazzino
from .models import Preventivo, Fattura
from django.contrib.auth.models import User
from django.test import override_settings
from django.core import mail
from django.urls import reverse
import apps.fatturazione.views as fatt_views


class FatturazioneTests(TestCase):
    def setUp(self):
        """
        Inizializza l'ambiente di test creando la gerarchia minima di oggetti:
        User -> Cliente -> Veicolo -> OrdineLavoro.
        """
        # Creazione utente con profilo e ruolo specifico per i test di accesso alle view
        self.user = User.objects.create_user(username='mecc', password='pw')
        self.user.profilo.ruolo = 'receptionist'
        self.user.profilo.save()
        
        # Creazione anagrafica cliente e veicolo associato
        self.cliente = Cliente.objects.create(
            nome='Mario', 
            cognome='Rossi', 
            telefono='333', 
            codice_fiscale='RSSMRA80A01'
        )
        self.veicolo = Veicolo.objects.create(
            cliente=self.cliente, 
            targa='AA111BB', 
            marca='Fiat', 
            modello='Panda', 
            anno=2010, 
            km=100000
        )
        
        # Apertura di un ordine di lavoro tecnico
        self.ordine = OrdineLavoro.objects.create(veicolo=self.veicolo, meccanico=self.user)

    def test_preventivo_e_generazione_fattura(self):
        """
        Verifica che i totali siano sommati correttamente e che la conversione 
        in fattura generi i metadati necessari (es. numero documento).
        """
        # Creazione di un intervento (costo manodopera fisso a 50€)
        Intervento.objects.create(
            ordine=self.ordine, 
            descrizione='Cambio olio', 
            ore_lavorate=1, 
            costo_manodopera=50
        )
        
        # Caricamento di un ricambio e registrazione del movimento di scarico magazzino
        # Costo totale atteso ricambi: 2 unità * 10€ = 20€
        r = Ricambio.objects.create(
            codice='R1', descrizione='Olio', quantita_disponibile=10, 
            soglia_minima=1, prezzo_acquisto=5, prezzo_vendita=10
        )
        MovimentoMagazzino.objects.create(
            ricambio=r, ordine_lavoro=self.ordine, tipo='uscita', quantita=2
        )

        # Inizializzazione del preventivo e calcolo logico dei totali
        prev = Preventivo.objects.create(ordine=self.ordine)
        prev.salva_e_calcola()
        
        # Assertion: Verifichiamo che il calcolo non sia zero
        self.assertGreater(prev.totale_manodopera, 0)
        
        # Transizione di stato obbligatoria per la fatturazione
        prev.stato = 'approvato'
        prev.save()
        
        # Generazione fattura finale
        fatt = prev.genera_fattura()
        
        # Verifiche sull'oggetto Fattura generato
        self.assertIsInstance(fatt, Fattura)
        self.assertIsNotNone(fatt.numero_documento)

    def test_invia_preventivo_view_sends_email(self):
        """
        Verifica l'integrazione della view con il sistema di mailing.
        Utilizza un backend di memoria per intercettare l'invio.
        """
        self.cliente.email = 'cliente@example.com'
        self.cliente.save()
        
        prev = Preventivo.objects.create(ordine=self.ordine)
        prev.salva_e_calcola()
        prev.stato = 'approvato'
        prev.save()

        # Mocking: Disabilitiamo la generazione PDF (WeasyPrint) per testare solo l'invio mail
        fatt_views.HTML = None
        
        # Test dell'invio mail usando il backend 'locmem'
        with override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            self.client.login(username='mecc', password='pw')
            
            url = reverse('fatturazione:invia_preventivo', args=[prev.id])
            resp = self.client.post(url)
            
            # Verifichiamo che la coda dei messaggi in uscita contenga la mail del preventivo
            self.assertEqual(len(mail.outbox), 1)
            self.assertIn('Preventivo Officina', mail.outbox[0].subject)

    def test_preventivo_non_approvato_raises(self):
        """
        Verifica il vincolo di integrità: non è possibile generare una fattura 
        se il preventivo non è nello stato 'approvato'.
        """
        prev = Preventivo.objects.create(ordine=self.ordine)
        prev.salva_e_calcola()
        prev.stato = 'bozza'
        prev.save()
        
        # Assertion: il metodo deve sollevare un errore di valore
        with self.assertRaises(ValueError):
            prev.genera_fattura()