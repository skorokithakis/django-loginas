django-loginas
==============

About
-----

"Login as user" for the Django admin.

[![PyPI version](https://img.shields.io/pypi/v/django-loginas.svg)](https://pypi.python.org/pypi/django-loginas)

`loginas` supports Python 3 only, as of version 0.4. If you're on 2, use
[0.3.6](https://pypi.org/project/django-loginas/0.3.6/).


Installing django-loginas
-------------------------

* Add `loginas` to your Python path, or install using pip: `pip install django-loginas`

* Add the `loginas` app to your `INSTALLED_APPS`:

```python
# settings.py
INSTALLED_APPS = [... 'loginas', ...]
```

* Add the `loginas` URL to your `urls.py`:

```python
# urls.py
urlpatterns = [
    # from Django 3.2 on, make sure to add loginas urls before the admin site urls, i.e.:
    path('admin/', include('loginas.urls')),
    path('admin/', admin.site.urls),
]
```

* If you're using a custom User model, you'll need to add the template to it so the button shows up:

```python
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

```python
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

```python
# settings.py

LOGINAS_REDIRECT_URL = '/loginas-redirect-url'
```

In order to automatically restore the original user upon log out, replace the default log out
with a special log out that restores the original login session from a signed session.

```python
# settings.py

from django.core.urlresolvers import reverse_lazy
LOGOUT_URL = reverse_lazy('loginas-logout')
```

Additionally, you can specify the redirect url for logout (the default is `settings.LOGIN_REDIRECT_URL`).

```python
# settings.py

from django.core.urlresolvers import reverse_lazy
LOGINAS_LOGOUT_REDIRECT_URL = reverse_lazy('admin:index')
```

By default, clicking "Login as user" will not update `user.last_login`.
You can override this behavior like so:

```python
# settings.py

LOGINAS_UPDATE_LAST_LOGIN = True
```

By default, the login switch message will generate [Django admin `LogEntry`](https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#logentry-objects) messages using the `User` model's
`USERNAME_FIELD` like `f"User {impersonator_user.getattr(USERNAME_FIELD)} logged in as {impersonated_user.getattr(USERNAME_FIELD)}."` You can override this behavior by passing in a different
field name:

```python
# settings.py

LOGINAS_USERNAME_FIELD = 'email'
```

Other implementation suggestions
--------------------------------

### Existing logout view?

If you already have a logout view, you can modify to login the original user again after having had a "login as" session. Here's an example:

```python
class LogoutView(LogoutView):
    template_name = 'myapp/logged_out.html'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        from loginas.utils import restore_original_login
        restore_original_login(request)
        return redirect('myapp:login')
```

### Template awareness

You can add the context processor `loginas.context_processors.impersonated_session_status`
in your settings.py file if you'd like to be able to access a variable `is_impersonated_session`
in all your template contexts:

```python
# settings.py

TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                ...
                'loginas.context_processors.impersonated_session_status',
            ],
        },
    },
]
```

Note that django-loginas won't let you log in as other superusers, to prevent
privilege escalation from staff users to superusers. If you want to log in as
a superuser, first demote them to a non-superuser, and then log in.

License
-------

This software is distributed under the BSD license.
