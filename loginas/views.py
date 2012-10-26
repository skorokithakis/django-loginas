from django.conf import settings
from django.contrib import messages
from django.contrib.auth import load_backend, login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import HttpResponseBadRequest, HttpResponseRedirect


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
        current_user_pk = request.user.pk
        previous_users_pk = request.session.get("previous_users_pk", default=[])
        previous_users_pk.append(current_user_pk)
        login(request, user)
        request.session["previous_users_pk"] = previous_users_pk

    return redirect("/")


def loginas_exit(request):
    previous_users_pk = request.session.get("previous_users_pk", default=[])
    if not previous_users_pk:
        return HttpResponseBadRequest(("Admin never logged in as this user. Cannot exit loginas."))
    superuser = User.objects.get(pk=previous_users_pk[-1])
    superuser.backend = settings.AUTHENTICATION_BACKENDS[0]
    login(request, superuser)
    request.session["previous_users_pk"] = previous_users_pk[:-1]
    return HttpResponseRedirect(getattr(settings, "LOGINAS_EXIT_URL", "/"))
