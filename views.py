from django.conf import settings
from django.contrib import messages
from django.contrib.auth import load_backend, login
from django.contrib.auth.models import User
from django.shortcuts import redirect


def user_login(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "You need to be a superuser to do that.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    user = User.objects.get(pk=user_id)

    # Find a suitable backend.
    if not hasattr(user, 'backend'):
        for backend in settings.AUTHENTICATION_BACKENDS:
            if user == load_backend(backend).get_user(user.pk):
                user.backend = backend
                break

    # Log the user in.
    if hasattr(user, 'backend'):
        login(request, user)

    return redirect("/")
