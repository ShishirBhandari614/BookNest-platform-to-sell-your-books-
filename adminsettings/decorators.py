# userauth/decorators.py

from functools import wraps
from django.http import JsonResponse, HttpResponseForbidden
from rest_framework_simplejwt.tokens import AccessToken
from authentication.models import CustomUser  # adjust if needed
from django.contrib.auth.decorators import login_required

def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("You are not authorized to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
