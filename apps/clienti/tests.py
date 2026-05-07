"""Test per il CRUD dei `Veicolo` tramite le view pubbliche di `clienti`.

Questo test verifica che un utente con ruolo `receptionist` possa creare
un veicolo via POST verso la view dedicata.
"""

# Importazione dei moduli necessari per i test di Django, la gestione degli URL e i modelli
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Cliente, Veicolo


class VeicoloCRUDTests(TestCase):
    def setUp(self):
        """Inizializzazione dei dati necessari per ogni metodo di test."""
        # Inizializza il client per simulare le richieste HTTP
        self.client = Client()
        
        # Crea un'istanza di Cliente nel database di test
        self.cliente = Cliente.objects.create(
            nome='Luca', 
            cognome='Bianchi', 
            telefono='321', 
            codice_fiscale='BNCLCU80A01H501U'
        )
        
        # Crea un utente per l'autenticazione
        self.user = User.objects.create_user(username='reception', password='pass')
        
        # Imposta il ruolo dell'utente a 'receptionist' e salva il profilo associato
        self.user.profilo.ruolo = 'receptionist'
        self.user.profilo.save()

    def test_crea_veicolo_via_view(self):
        """Verifica la creazione di un veicolo tramite una richiesta POST alla view."""
        # Esegue il login dell'utente creato nel setUp
        logged = self.client.login(username='reception', password='pass')
        self.assertTrue(logged) # Verifica che il login sia andato a buon fine
        
        # Genera l'URL per la view di creazione veicolo, passando la chiave primaria del cliente
        url = reverse('clienti:crea_veicolo', args=[self.cliente.pk])
        
        # Dati del nuovo veicolo da inviare nel corpo della richiesta
        data = {
            'cliente': str(self.cliente.pk),
            'targa': 'CC222DD',
            'marca': 'Ford',
            'modello': 'Focus',
            'anno': '2015',
            'km': '50000'
        }
        
        # Invia una richiesta POST all'URL con i dati sopra definiti
        resp = self.client.post(url, data)
        
        # Verifica che nel database esista esattamente un veicolo con la targa specificata
        self.assertEqual(Veicolo.objects.filter(targa='CC222DD').count(), 1)