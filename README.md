django-loginas
==============

About
-----

"Login as user" for the Django admin.

[![Build Status](https://secure.travis-ci.org/stochastic-technologies/django-loginas.png?branch=master)](http://travis-ci.org/stochastic-technologies/django-loginas)


Installing django-loginas
-------------------------

* Add `loginas` to your Python path, or install using pip: `pip install django-loginas`

* Add the `loginas` app to your `INSTALLED_APPS`:

```
# settings.py
INSTALLED_APPS = (... 'loginas', ...)
```

* Add the loginas URL to your `urls.py`:

```
# urls.py
urlpatterns += patterns('loginas.views',
    url(r"^login/user/(?P<user_id>.+)/$", "user_login", name="loginas-user-login"),
)
```

* At this point, the only users who will be able to log in as other users are those with the `is_superuser` permission.
If you use custom User models, and haven't specified that permission, or if you want to change which users are
authorized to log in as others, you can define the `CAN_LOGIN_AS` setting, like so:

```
# settings.py

# This will only allow admins to log in as other users:
CAN_LOGIN_AS = lambda request, target_user: request.user.is_admin

# This will only allow admins to log in as other users, as long as
# those users are not admins themselves:
CAN_LOGIN_AS = lambda request, target_user: request.user.is_admin and not target_user.is_admin

# You can also define a string path to a module:
CAN_LOGIN_AS = "utils.helpers.custom_loginas"
```

At this point, you should be good to go. Just visit the Django admin, navigate to a user and you should see the "Log
in as user" button at the top right of the screen.

License
-------

This software is distributed under the BSD license.
