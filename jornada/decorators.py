from django.http import HttpResponseForbidden
from functools import wraps

def solo_academicos(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'academico'):
            return HttpResponseForbidden("Acceso restringido a académicos.")
        return view_func(request, *args, **kwargs)
    return wrapper
