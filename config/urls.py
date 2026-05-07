"""Router principale delle URL del progetto.

Questo modulo include gli URL delle applicazioni interne e le view di
autenticazione fornite da Django. Manteniamo la root ('') puntata alla
dashboard dell'app `officina`.
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Interfaccia di amministrazione avanzata di Django
    path('admin/', admin.site.urls),
    
    # HOME PAGE: Reindirizza direttamente alla dashboard dell'officina.
    # Essendo la stringa vuota '', è il punto di ingresso (es: www.tuogestionale.it/)
    path('', include('apps.officina.urls')), 
    
    # MODULI APPLICATIVI: Ogni riga include gli URL specifici delle sottocartelle
    path('clienti/', include('apps.clienti.urls')),
    path('magazzino/', include('apps.magazzino.urls')),
    path('fatturazione/', include('apps.fatturazione.urls')),
    
    # AUTENTICAZIONE: Gestione sicura di Login e Logout.
    # Usiamo le viste predefinite di Django, puntando al tuo template personalizzato.
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]