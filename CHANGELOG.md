# Changelog

Tutte le modifiche rilevanti per questa serie di patch.

## [Unreleased]
- Implementazione completa di `Profilo` utente con ruoli (`titolare`, `meccanico`, `receptionist`).
- Decorator `role_required` e middleware `RestrictAdminMiddleware` per controllo accessi.
- `apps/clienti`: CRUD `Cliente`/`Veicolo`, form e template; aggiunta CRUD veicolo e test.
- `apps/officina`: `OrdineLavoro`, `Intervento`, form inline per interventi e ricambi nella scheda ordine; view per aggiungere/rimuovere ricambi usati; protezione accessi per meccanici.
- `apps/magazzino`: `Ricambio`, `MovimentoMagazzino` (aggiorna giacenze su save/delete), `RicambioUsato` collegato a `MovimentoMagazzino`; migration `0002_create_ricambio_usato.py`.
- `apps/fatturazione`: `Preventivo`/`Fattura` logica, calcolo totali, generazione fattura da preventivo.
- Test aggiunti: integrazione magazzino (entrata/uscita/delete/update), officina (intervento, permessi), clienti (CRUD veicolo), fatturazione (preventivo->fattura, email, casi di errore).
- Template aggiunti/aggiornati per dettaglio ordine, form intervento, form veicolo, conferma cancellazione ricambio.
- CI: GitHub Actions workflow per eseguire migrazioni e test su push/PR.
- Script utili: `scripts/setup_and_test.ps1`, `scripts/git_commit_and_push.ps1`.
- Documentazione: `README.md` aggiornato con WeasyPrint/SMTP e comandi di setup; `PULL_REQUEST_DRAFT.md` e `PR_COMMANDS.md` inclusi.

## Note breaking / da verificare
- `RicambioUsato` aggiunge campo `movimento` e richiede migrazioni locali.
- WeasyPrint richiede librerie native su Windows (consigliato WSL o container Linux per generazione PDF affidabile).

## How to release
1. Eseguire tutti i test locali.
2. Creare branch e PR (vedi `PR_COMMANDS.md`).
3. Assicurarsi che CI passi e revisionare PR.
4. Mergiare e creare tag di release se necessario.
