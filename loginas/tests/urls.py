from django.conf.urls.defaults import *

urlpatterns = patterns('loginas.tests.views',
    url(r"^current_user/$", "current_user", name="current_user"),
    url(r"^", include('loginas.urls')),
)
