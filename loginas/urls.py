from django.urls import path

from loginas.views import user_login
from loginas.views import user_logout

urlpatterns = [
    path("login/user/<str:user_id>/", user_login, name="loginas-user-login"),
    path("logout/", user_logout, name="loginas-logout"),
]
