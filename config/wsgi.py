"""
WSGI config for config project.
Espone la variabile 'application', che il server userà per far girare il progetto.
"""

import os
from django.core.wsgi import get_wsgi_application

# Specifichiamo dove Django deve andare a cercare le impostazioni (settings.py).
# In questo caso, punta alla cartella 'config'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Crea l'oggetto 'application', il vero e proprio motore che riceve le richieste
# degli utenti e restituisce le pagine del gestionale.
application = get_wsgi_application()