django-loginas
==============

About
-----

"Log in as user" for the Django admin.


Installing django-loginas
-------------------------

1. Add `loginas` to your Python path.

2. Add the `loginas` app to your `INSTALLED_APPS`:

```
# settings.py
INSTALLED_APPS = (... 'loginas', ...)
```

3. Add the loginas URL to your `urls.py`:

```
# urls.py
urlpatterns += patterns('loginas.views',
    url(r"^login/user/(?P<user_id>.+)/$", "user_login", name="loginas-user-login"),
)
```

And you should be good to go. Just visit the Django admin, navigate to a user and you should see the "Log in as user"
button at the top right of the screen.

License
-------

This software is distributed under the BSD license.
