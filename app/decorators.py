from functools import wraps
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseForbidden


def staff_required(view_func):
    @login_required
    @wraps(view_func)
    def wrapper(request: HttpRequest, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("You do not have permission to access this page.")
        return view_func(request, *args, **kwargs)

    return wrapper
