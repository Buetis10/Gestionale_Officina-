"""Test per il modulo magazzino.

Contiene verifiche automatiche per i movimenti di magazzino e per
la sincronizzazione tra `RicambioUsato` e `MovimentoMagazzino`.
"""

from django.test import TestCase
from .models import Ricambio, MovimentoMagazzino


class MagazzinoTests(TestCase):
    def test_movimento_entrata_aggiorna_giacenza(self):
        r = Ricambio.objects.create(codice='ABC1', descrizione='Pasticche', quantita_disponibile=0, soglia_minima=2, prezzo_acquisto=10, prezzo_vendita=20)
        m = MovimentoMagazzino.objects.create(ricambio=r, tipo='entrata', quantita=5)
        r.refresh_from_db()
        self.assertEqual(r.quantita_disponibile, 5)

    def test_movimento_uscita_riduce_giacenza(self):
        r = Ricambio.objects.create(codice='ABC2', descrizione='Filtro', quantita_disponibile=10, soglia_minima=2, prezzo_acquisto=5, prezzo_vendita=8)
        m = MovimentoMagazzino.objects.create(ricambio=r, tipo='uscita', quantita=3)
        r.refresh_from_db()
        self.assertEqual(r.quantita_disponibile, 7)

    def test_delete_movimento_ripristina_giacenza(self):
        r = Ricambio.objects.create(codice='DEL1', descrizione='Test', quantita_disponibile=5, soglia_minima=1, prezzo_acquisto=1, prezzo_vendita=2)
        m = MovimentoMagazzino.objects.create(ricambio=r, tipo='entrata', quantita=4)
        r.refresh_from_db()
        self.assertEqual(r.quantita_disponibile, 9)
        # cancellando il movimento, la giacenza viene ripristinata
        m.delete()
        r.refresh_from_db()
        self.assertEqual(r.quantita_disponibile, 5)

from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.clienti.models import Cliente, Veicolo
from apps.officina.models import OrdineLavoro
from .models import Ricambio


class RicambioUsatoViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.cliente = Cliente.objects.create(nome='Anna', cognome='Verdi', telefono='111', codice_fiscale='VRDANN80A01H501U')
        self.veicolo = Veicolo.objects.create(cliente=self.cliente, targa='EE333FF', marca='Opel', modello='Corsa', anno=2012)
        self.user = User.objects.create_user(username='mecc2', password='pass')
        self.user.profilo.ruolo = 'meccanico'
        self.user.profilo.save()
        self.ordine = OrdineLavoro.objects.create(veicolo=self.veicolo)
        self.ricambio = Ricambio.objects.create(codice='RIC001', descrizione='Filtro olio', quantita_disponibile=10, soglia_minima=2, prezzo_acquisto=5, prezzo_vendita=12.50)

    def test_aggiungi_ricambio_via_post(self):
        logged = self.client.login(username='mecc2', password='pass')
        self.assertTrue(logged)
        url = reverse('officina:aggiungi_ricambio', args=[self.ordine.pk])
        data = {'ricambio': str(self.ricambio.pk), 'quantita': '2'}
        resp = self.client.post(url, data)
        # dopo il POST, dovrebbe esserci una istanza di RicambioUsato collegata all'ordine
        from apps.magazzino.models import RicambioUsato
        self.assertEqual(RicambioUsato.objects.filter(ordine_lavoro=self.ordine).count(), 1)

    def test_delete_ricambio_usato_elimina_movimento(self):
        # crea ricambio usato tramite istanza -> movimento creato automaticamente
        from apps.magazzino.models import RicambioUsato, MovimentoMagazzino
        ru = RicambioUsato.objects.create(ricambio=self.ricambio, ordine_lavoro=self.ordine, quantita=2, prezzo_unitario=12.50)
        # movimento creato e collegato
        self.assertIsNotNone(ru.movimento)
        mov_pk = ru.movimento.pk
        # cancella il ricambio usato
        ru.delete()
        # movimento deve essere cancellato
        self.assertFalse(MovimentoMagazzino.objects.filter(pk=mov_pk).exists())

    def test_update_movimento_aggiorna_giacenza(self):
        r = Ricambio.objects.create(codice='UPD1', descrizione='UpdateTest', quantita_disponibile=10, soglia_minima=1, prezzo_acquisto=1, prezzo_vendita=2)
        m = MovimentoMagazzino.objects.create(ricambio=r, tipo='entrata', quantita=5)
        r.refresh_from_db()
        self.assertEqual(r.quantita_disponibile, 15)
        # aggiorniamo il movimento: da 5 a 2 -> la giacenza deve ridursi di 3
        m.quantita = 2
        m.save()
        r.refresh_from_db()
        self.assertEqual(r.quantita_disponibile, 12)

    def test_update_ricambio_usato_updates_movimento(self):
        from apps.magazzino.models import RicambioUsato, MovimentoMagazzino
        ru = RicambioUsato.objects.create(ricambio=self.ricambio, ordine_lavoro=self.ordine, quantita=2, prezzo_unitario=12.50)
        self.assertIsNotNone(ru.movimento)
        mov = MovimentoMagazzino.objects.get(pk=ru.movimento.pk)
        self.assertEqual(mov.quantita, 2)
        # aggiorniamo la quantita' del ricambio usato
        ru.quantita = 1
        ru.save()
        mov.refresh_from_db()
        self.assertEqual(mov.quantita, 1)
