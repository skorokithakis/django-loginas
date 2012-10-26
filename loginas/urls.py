from django.conf.urls.defaults import *

urlpatterns = patterns('loginas.views',
    url(r"^login/user/(?P<user_id>.+)/$", "user_login", name="loginas-user-login"),
    url(r"^loginas_exit/?$", "loginas_exit", name="loginas_exit")
)
