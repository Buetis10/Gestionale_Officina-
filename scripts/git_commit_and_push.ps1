# Script PowerShell per creare branch, commit e push
# Esegui dalla root del progetto:
# .\scripts\git_commit_and_push.ps1

param(
    [string]$branchName = "feature/align-to-traccia",
    [string]$commitFile = "COMMIT_MESSAGE.txt"
)

Write-Host "Creazione branch: $branchName"
git checkout -b $branchName

Write-Host "Aggiungo tutte le modifiche"
git add .

if (Test-Path $commitFile) {
    Write-Host "Commit usando il file $commitFile"
    git commit -F $commitFile
} else {
    Write-Host "File $commitFile non trovato. Inserisci un messaggio di commit inline."
    git commit -m "Allineamento progetto alla traccia"
}

Write-Host "Push del branch verso origin"
git push -u origin $branchName

Write-Host "Fine. Crea una Pull Request dal branch $branchName se necessario."
