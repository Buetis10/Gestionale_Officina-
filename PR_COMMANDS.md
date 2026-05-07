# Comandi per creare branch, push e Pull Request (GitHub)

Esegui questi comandi nella root del progetto dopo aver verificato che i test siano passati localmente.

1) Crea branch e committa (se non lo hai già fatto):

```powershell
# Assumi che tu sia nella root del repo
git checkout -b feature/align-to-traccia
git add .
git commit -F COMMIT_MESSAGE.txt
```

2) Push del branch remoto:

```powershell
git push -u origin feature/align-to-traccia
```

3) Creare PR (usando GitHub CLI `gh`):

```powershell
# Se non sei loggato esegui 'gh auth login' e segui le istruzioni
gh pr create --title "Allineamento progetto alla traccia" --body-file PULL_REQUEST_DRAFT.md --base main --head feature/align-to-traccia --draft
```

4) (Opzionale) Aprire PR nel browser:

```powershell
gh pr view --web
```

Note:
- Se il branch principale remoto si chiama `master` usa `--base master`.
- `gh` richiede autenticazione; usa un token con permessi `repo`.
- Il workflow CI è attivato su push/PR e eseguirà migrazioni + test automaticamente.

Se preferisci, posso preparare un comando `gh pr create` che apre la PR non in draft (rimuovi `--draft`).
