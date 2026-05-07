"""Impostazioni principali del progetto.

Questo file contiene la configurazione Django usata in sviluppo:
- registrazione delle app
- middleware
- database SQLite per ambiente locale
- impostazioni email di sviluppo (console)

Non inserire segreti di produzione qui: usa variabili d'ambiente.
"""

import os
import sys
from pathlib import Path

# BASE_DIR: Definisce dove si trova il progetto sul tuo computer.
BASE_DIR = Path(__file__).resolve().parent.parent

# NOTA: non modificare il `sys.path` qui: Django carica le app tramite il
# valore `name` in ciascun AppConfig (es. 'apps.clienti') e alterare il
# percorso può causare che i moduli siano importati con nomi diversi
# (es. 'clienti' invece di 'apps.clienti'), rompendo i test e l'app registry.

# --- SICUREZZA ---
SECRET_KEY = 'django-insecure-!(8^&nzcn)df#58_jugy!u0y@o)lquer@4&ipej1+jde_o0y2*'
DEBUG = True
ALLOWED_HOSTS = ['*']  # Permetti l'accesso dalla rete locale in sviluppo

# --- REGISTRO DELLE APPLICAZIONI ---
INSTALLED_APPS = [
    'apps.utenti.apps.UtentiConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Le tue app core
    'apps.clienti',
    'apps.magazzino',
    'apps.fatturazione',
    'apps.officina',
    
    # Plugin per l'estetica
    'crispy_forms',
    'crispy_bootstrap5',
]

# --- MIDDLEWARE (CORREZIONE: AGGIUNTA QUESTA SEZIONE) ---
# I middleware sono necessari per gestire sessioni, utenti e messaggi nell'admin.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Middleware custom: limita accesso admin al ruolo titolare
MIDDLEWARE.insert(len(MIDDLEWARE), 'apps.utenti.middleware.RestrictAdminMiddleware')

# Indica a Django dove si trova il file delle rotte principali
ROOT_URLCONF = 'config.urls'

# --- TEMPLATES ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# --- DATABASE ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- PASSWORD VALIDATION ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- INTERNAZIONALIZZAZIONE ---
LANGUAGE_CODE = 'it-it'  # Impostato in italiano
TIME_ZONE = 'Europe/Rome' # Impostato fuso orario Italia
USE_I18N = True
USE_TZ = True

# --- FILE STATICI ---
STATIC_URL = 'static/'

# EMAIL (sviluppo): invia email sul terminale / console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'officina@example.com'

# --- CONFIGURAZIONE CRISPY FORMS ---
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# --- FLUSSO DI NAVIGAZIONE ---
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'officina:dashboard'
LOGOUT_REDIRECT_URL = 'login'

# Valore predefinito per le chiavi primarie
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'