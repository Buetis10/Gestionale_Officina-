# Bozza Pull Request: Allineamento progetto alla traccia

## Descrizione
Questa PR allinea il progetto alla traccia fornita dall'utente: implementa modelli, view, permessi, form inline, gestione magazzino automatica, generazione PDF base e test di integrazione per le funzionalità principali.

## Modifiche principali
- `apps/utenti`: `Profilo`, signals e decorator `role_required` (controllo ruoli)
- `apps/clienti`: CRUD `Cliente`/`Veicolo`, form, template e test per CRUD veicolo
- `apps/officina`: `OrdineLavoro`, `Intervento`, view per aggiungere interventi/ricambi, form inline, rimozione ricambi usati
- `apps/magazzino`: `Ricambio`, `MovimentoMagazzino`, `RicambioUsato` (movimento collegato e delete sync)
- `apps/fatturazione`: `Preventivo`/`Fattura` logica, generazione fattura, test corretti
- Template aggiuntivi: dettagli ordine, form intervento, confirm delete
- Test aggiuntivi per magazzino, officina, clienti
- `README.md` aggiornato con istruzioni WeasyPrint/SMTP
- Script `scripts/setup_and_test.ps1` e `scripts/git_commit_and_push.ps1`
- Migration aggiunta: `apps/magazzino/migrations/0002_create_ricambio_usato.py`

## Checklist
- [ ] Eseguite migrazioni locali
- [ ] Eseguiti i test locali: `python manage.py test`
- [ ] Verificato WeasyPrint in ambiente di sviluppo (dipendenze native)
- [ ] Creata pull request su repository remoto

## Note tecniche e raccomandazioni
- Ho creato la migration per `RicambioUsato`; eseguire `python manage.py migrate`.
- WeasyPrint richiede librerie C (GTK/Cairo) su Windows — si consiglia l'uso di WSL o container per la generazione PDF in ambiente di sviluppo.

## Comandi consigliati (locale)
```powershell
# setup
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# migrazioni e test
python manage.py makemigrations
python manage.py migrate
python manage.py test

# commit e push (script)
.\scripts\git_commit_and_push.ps1
```

---

Se vuoi, creo la Pull Request draft direttamente (richiederà il tuo token o accesso remoto), oppure ti lascio i comandi per farlo localmente. Dimmi come preferisci procedere.
