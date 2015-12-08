from django.conf.urls import *
from loginas.views import user_login

urlpatterns = [
    url(r"^login/user/(?P<user_id>.+)/$", user_login, name="loginas-user-login"),
]
