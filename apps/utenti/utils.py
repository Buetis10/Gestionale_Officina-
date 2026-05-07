"""Utility per l'autorizzazione basata su ruoli.

Questo modulo permette di proteggere le diverse sezioni dell'officina 
(es. impedire che un meccanico acceda alle fatture del titolare).
"""

from functools import wraps
from django.http import HttpResponseForbidden


def role_required(allowed_roles):
    """
    DECORATORE PER VIEW A FUNZIONE:
    Si usa sopra le funzioni (es. @role_required(['titolare'])).
    """
    # 1. Normalizzazione: trasforma stringhe o liste in un set a caratteri minuscoli
    # per evitare errori se qualcuno scrive "Titolare" invece di "titolare".
    if isinstance(allowed_roles, str):
        allowed = {allowed_roles.lower()}
    else:
        allowed = {r.lower() for r in allowed_roles}

    def decorator(view_func):
        @wraps(view_func) # Mantiene i metadati della funzione originale
        def _wrapped(request, *args, **kwargs):
            user = request.user
            
            # 2. Controllo Autenticazione: se l'utente non ha fatto login, blocca subito
            if not user.is_authenticated:
                return HttpResponseForbidden('Accesso negato')
            
            # 3. Bypass Superuser: l'amministratore di sistema ha sempre accesso a tutto
            if getattr(user, 'is_superuser', False):
                return view_func(request, *args, **kwargs)

            # 4. Verifica Ruolo: cerca il ruolo nel profilo utente e lo confronta con quelli permessi
            profilo = getattr(user, 'profilo', None)
            ruolo = getattr(profilo, 'ruolo', None)
            
            if ruolo and ruolo.lower() in allowed:
                return view_func(request, *args, **kwargs)
            
            # Se il ruolo non è tra quelli ammessi, restituisce l'errore 403 (Forbidden)
            return HttpResponseForbidden('Accesso negato: ruolo insufficiente')
        return _wrapped
    return decorator


class RoleRequiredMixin:
    """
    MIXIN PER CLASS-BASED VIEWS (CBV):
    Fornisce la stessa logica del decoratore ma per le classi.
    """
    required_roles = None

    def dispatch(self, request, *args, **kwargs):
        """
        Metodo dispatch: è il punto di ingresso della richiesta nella classe.
        Qui eseguiamo i controlli di sicurezza prima di mostrare la pagina.
        """
        # Controllo login
        if not request.user.is_authenticated:
            return HttpResponseForbidden('Accesso negato')
        
        # Bypass per superuser
        if getattr(request.user, 'is_superuser', False):
            return super().dispatch(request, *args, **kwargs)

        profilo = getattr(request.user, 'profilo', None)
        ruolo = getattr(profilo, 'ruolo', None)
        
        if self.required_roles:
            # Normalizzazione dei ruoli richiesti nella classe
            allowed = {self.required_roles.lower()} if isinstance(self.required_roles, str) else {r.lower() for r in self.required_roles}
            
            if ruolo and ruolo.lower() in allowed:
                return super().dispatch(request, *args, **kwargs)
            
            return HttpResponseForbidden('Accesso negato: ruolo insufficiente')
        
        # Se non sono specificati ruoli richiesti, permette l'accesso (comportamento standard)
        return super().dispatch(request, *args, **kwargs)