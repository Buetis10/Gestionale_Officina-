"""ASGI entrypoint del progetto.

Questo file espone l'oggetto ``application`` usato dai server ASGI.
Serve come ponte tra il server ASGI (es. Daphne, Uvicorn) e Django.
Non contiene logica applicativa: è pensato solo per il deployment.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
