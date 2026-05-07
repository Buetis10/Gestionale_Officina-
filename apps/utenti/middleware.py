from django.http import HttpResponseForbidden


class RestrictAdminMiddleware:
    """Restringe l'accesso a /admin/ agli utenti con ruolo 'titolare' o ai superuser.
    Utile per mantenere l'admin Django accessibile solo al titolare in ambiente di produzione.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path.startswith('/admin/'):
            user = getattr(request, 'user', None)
            if user is None or not user.is_authenticated:
                return HttpResponseForbidden('Accesso all\'admin negato')
            # permetti al superuser o al titolare
            profilo = getattr(user, 'profilo', None)
            if not (user.is_superuser or (profilo and getattr(profilo, 'ruolo', None) == 'titolare')):
                return HttpResponseForbidden('Accesso all\'admin riservato al titolare')

        return self.get_response(request)
