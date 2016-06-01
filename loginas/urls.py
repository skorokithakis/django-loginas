from django.conf.urls import url
from loginas.views import user_login, user_logout

urlpatterns = [
    url(r"^login/user/(?P<user_id>.+)/$", user_login, name="loginas-user-login"),
    url(r"^logout/$", user_logout, name="loginas-logout"),
]
