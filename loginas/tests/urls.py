from django.urls import include
from django.urls import path

from loginas.tests import views

urlpatterns = [
    path("", views.index, name="index"),
    path("current_user/", views.current_user, name="current_user"),
    path("", include("loginas.urls")),
]
