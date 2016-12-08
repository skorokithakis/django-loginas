django-loginas
==============

About
-----

"Login as user" for the Django admin.

[![Build Status](https://secure.travis-ci.org/skorokithakis/django-loginas.png?branch=master)](http://travis-ci.org/skorokithakis/django-loginas)


Installing django-loginas
-------------------------

* Add `loginas` to your Python path, or install using pip: `pip install django-loginas`

* Add the `loginas` app to your `INSTALLED_APPS`:

```
# settings.py
INSTALLED_APPS = [... 'loginas', ...]
```

* Add the loginas URL to your `urls.py`:

```
# urls.py
urlpatterns += url(r'^admin/', include('loginas.urls')),
```

* If you're using a custom User model, you'll need to add the template to it so the button shows up:

```
# admin.py
class YourUserAdmin(ModelAdmin):
    change_form_template = 'loginas/change_form.html'
```

At this point, you should be good to go. Just visit the Django admin, navigate to a user and you should see the "Log
in as user" button at the top right of the screen.

Configuring
-----------

At this point, the only users who will be able to log in as other users are those with the `is_superuser` permission.
If you use custom User models, and haven't specified that permission, or if you want to change which users are
authorized to log in as others, you can define the `CAN_LOGIN_AS` setting, like so:

```
# settings.py

# This will only allow admins to log in as other users:
CAN_LOGIN_AS = lambda request, target_user: request.user.is_superuser

# This will only allow admins to log in as other users, as long as
# those users are not admins themselves:
CAN_LOGIN_AS = lambda request, target_user: request.user.is_superuser and not target_user.is_superuser

# You can also define a string path to a module:
CAN_LOGIN_AS = "utils.helpers.custom_loginas"
```

By default, clicking "Login as user" will send the user to `settings.LOGIN_REDIRECT_URL`.
You can override this behavior like so:

```
# settings.py

LOGINAS_REDIRECT_URL = '/loginas-redirect-url'
```

In order to automatically restore the original user upon log out, replace the default log out
with a special log out that restores the original login session from a signed session.

```
# settings.py

from django.core.urlresolvers import reverse_lazy
LOGOUT_URL = reverse_lazy('loginas-logout')
```

Additionally, you can specify the redirect url for logout (the default is `settings.LOGIN_REDIRECT_URL`).

```
# settings.py

from django.core.urlresolvers import reverse_lazy
LOGINAS_LOGOUT_REDIRECT_URL = reverse_lazy('admin:index')
```

By default, clicking "Login as user" will not update `user.last_login`.
You can override this behavior like so:

```
# settings.py

LOGINAS_UPDATE_LAST_LOGIN = True
```

Note that django-loginas won't let you log in as other superusers, to prevent
privilege escalation from staff users to superusers. If you want to log in as
a superuser, first demote them to a non-superuser, and then log in.

License
-------

This software is distributed under the BSD license.
