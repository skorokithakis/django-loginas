from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def index(request):
    return HttpResponse('')


def current_user(request):
    return HttpResponse(request.user.id)
