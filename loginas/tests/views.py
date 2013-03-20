from django.http import HttpResponse


def current_user(request):
    return HttpResponse(request.user.id)
