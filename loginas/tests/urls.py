from django.conf.urls import *
from loginas.tests import views

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^current_user/$", views.current_user, name="current_user"),
    url(r"^", include('loginas.urls')),
]
