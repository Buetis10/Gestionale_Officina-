"""Test funzionali per le view dell'app `officina`.

Verificano la creazione degli interventi e i controlli di accesso
per i meccanici sugli ordini a loro non assegnati.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.clienti.models import Cliente, Veicolo
from .models import OrdineLavoro, Intervento


class InterventoViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # crea cliente e veicolo
        self.cliente = Cliente.objects.create(nome='Mario', cognome='Rossi', telefono='123', codice_fiscale='RSSMRA80A01H501U')
        self.veicolo = Veicolo.objects.create(cliente=self.cliente, targa='AA111BB', marca='Fiat', modello='Panda', anno=2010)
        # crea utente meccanico
        self.user = User.objects.create_user(username='mecc', password='pass')
        self.user.profilo.ruolo = 'meccanico'
        self.user.profilo.save()
        # crea ordine
        self.ordine = OrdineLavoro.objects.create(veicolo=self.veicolo)

    def test_aggiungi_intervento_via_post(self):
        logged = self.client.login(username='mecc', password='pass')
        self.assertTrue(logged)
        url = reverse('officina:aggiungi_intervento', args=[self.ordine.pk])
        data = {'descrizione': 'Cambio olio', 'ore_lavorate': '1.50', 'costo_manodopera': '45.00'}
        resp = self.client.post(url, data)
        # dopo il POST, dovrebbe esserci almeno un intervento legato all'ordine
        self.assertEqual(Intervento.objects.filter(ordine=self.ordine).count(), 1)

    def test_meccanico_accesso_negato_su_altro_ordine(self):
        # crea un altro meccanico e assegna a un altro ordine
        other_user = User.objects.create_user(username='mecc_other', password='pass')
        other_user.profilo.ruolo = 'meccanico'
        other_user.profilo.save()
        ordine2 = OrdineLavoro.objects.create(veicolo=self.veicolo, meccanico=other_user)

        # login con il primo meccanico e tentativo di accesso a ordine2
        self.client.login(username='mecc', password='pass')
        url = reverse('officina:dettaglio_ordine', args=[ordine2.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)

