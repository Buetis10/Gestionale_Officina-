# Script di setup e test per Windows PowerShell
# Esegui in PowerShell dalla cartella del progetto:
# .\scripts\setup_and_test.ps1

$ErrorActionPreference = 'Stop'

Write-Host "Creazione virtualenv .venv..."
python -m venv .venv

Write-Host "Attivazione virtualenv..."
& .\.venv\Scripts\Activate.ps1

Write-Host "Installazione dipendenze..."
pip install --upgrade pip
pip install -r requirements.txt

Write-Host "Eseguo migrazioni..."
python manage.py makemigrations
python manage.py migrate

Write-Host "Esegue i test..."
python manage.py test

Write-Host "Comandi completati. Crea l'utente admin con: python manage.py createsuperuser"
Write-Host "Per avviare il server di sviluppo: python manage.py runserver 0.0.0.0:8000"
