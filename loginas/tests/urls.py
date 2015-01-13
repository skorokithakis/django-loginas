from django.conf.urls import *


urlpatterns = patterns('loginas.tests.views',
    url(r"^$", "index", name="index"),
    url(r"^current_user/$", "current_user", name="current_user"),
    url(r"^", include('loginas.urls')),
)
