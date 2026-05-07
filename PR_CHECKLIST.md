# PR Checklist

- [ ] Tutti i test locali passano (`python manage.py test`).
- [ ] Migrazioni generate e incluse (`python manage.py makemigrations`).
- [ ] Non ci sono modifiche sensibili al `settings.py` (SECRET_KEY, DEBUG in chiaro).
- [ ] Documentazione aggiornata (`README.md`, `CHANGELOG.md`).
- [ ] CI verde su GitHub Actions.
- [ ] PR descrive chiaramente le modifiche e i passi di test manuali.
- [ ] (Opzionale) Eseguire check di sicurezza/linters prima del merge.
