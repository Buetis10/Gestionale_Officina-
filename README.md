# Gestionale Officina

Progetto sviluppato durante il periodo di **tirocinio formativo** presso l'azienda **Staff S.p.A.**.

### 🛠 Descrizione del Progetto
L'obiettivo di questo software è la digitalizzazione dei processi operativi dell'officina. Il sistema permette di gestire l'intero ciclo di vita di una riparazione, dall'accettazione del veicolo fino alla generazione della fattura finale, passando per la gestione dinamica del magazzino ricambi.

### 🌟 Funzionalità principali implementate:
- **Dashboard di controllo:** Visualizzazione rapida dello stato degli ordini (In attesa, In lavorazione, Completati).
- **Ricerca Veicoli:** Sistema di ricerca immediata tramite targa per accedere allo storico interventi.
- **Gestione Magazzino:** Tracciamento dei ricambi utilizzati con aggiornamento automatico delle giacenze.
- **Interventi e Manodopera:** Registrazione dettagliata delle ore lavorate e delle operazioni effettuate.
- **Documentazione PDF:** Generazione automatica di fatture e preventivi pronti per la stampa.

---

## 🚀 Setup rapido sviluppo (Windows):

1. Crea virtualenv e attivalo

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Migrazioni e avvio server

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

Apri il browser su `http://<tuo_ip_locale>:8000/` per accedere dalla rete locale.

Note:
- `ALLOWED_HOSTS` è impostato a `['*']` per sviluppo locale; restringilo in produzione.
- Usa l'admin Django per creare `RicambioUsato` e `Preventivo` rapidamente.
 - Per eseguire i test unitari:

```powershell
python manage.py test
```

 - Dopo aver aggiunto nuovi modelli esegui:

```powershell
python manage.py makemigrations
python manage.py migrate
```

WeasyPrint (PDF):

- WeasyPrint richiede dipendenze native. Su Windows installa:

	- GTK3/GTK runtime e librerie di rendering (consultare la documentazione di WeasyPrint)
	- In alternativa, usa un container Linux dove `weasyprint` viene installato con le librerie di sistema.

SMTP / invio email:

- Per test locale rimane impostato `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`.
- Per invio reale configura in `config/settings.py` le variabili SMTP (`EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`) o usa provider come SendGrid.

Eseguire test e migrazioni (comandi consigliati):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py test
python manage.py runserver
```

**Checklist di deploy (sintetica)**

- Impostare `DEBUG=False` in `config/settings.py` e usare variabili d'ambiente per `SECRET_KEY`.
- Configurare `ALLOWED_HOSTS` in modo restrittivo.
- Configurare storage per `STATIC` e `MEDIA` (es. S3, Azure Blob, o server statico) e raccogliere gli static con `collectstatic`.
- Configurare server WSGI/ASGI (es. gunicorn/uvicorn) + reverse proxy (es. nginx) e HTTPS.
- Impostare servizio di mailbox SMTP/relay e aggiornare `EMAIL_*` in `config/settings.py`.
- Eseguire migrazioni e controllare backup DB prima del deploy.
- Verificare che WeasyPrint funzioni nell'ambiente di produzione (installare dipendenze di sistema su Linux).

