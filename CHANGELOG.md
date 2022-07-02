# Changelog


## Unreleased

### Features

* Redirect logouts to the 'next' url (#100) [Rodolfo Torres]

### Fixes

* Updates for Python 3.10 and Django 4.0 (#99) [Tom Carrick]


## v0.3.10 (2021-09-30)

### Fixes

* Modernize Django URL's (#93) [Adam Johnson]


## v0.3.8 (2019-12-05)

### Features

* Remove six and Py2 support. [Stavros Korokithakis]

### Fixes

* Don't crash when session doesn't exist (#86) [Gady Pitaru]

* Catch ImproperlyConfigured exc in user_login view (#85) [Sergei Zherevchuk]

* Add PermissionDenied support for `can_login_as` (#84) [Sergei Zherevchuk]


## v0.3.7 (2019-06-02)

### Features

* Change changelog format to Markdown. [Stavros Korokithakis]

* Drop Python 2 support. [Stavros Korokithakis]

### Fixes

* Don't require the messages framework (#80) [Jerome Leclanche]


## v0.3.4 (2018-04-17)

### Features

* Customize username field through settings.py (#72) [Eric Goddard]

### Fixes

* Constrain admin button to User model (#74) [Steve Kossouho]

* Skip backends that don't have a `get_user` method (#69) [Berk Birand]


## v0.3.2 (2017-05-18)

### Fixes

* Add 0.3.1 to changelog (#56) [Benjamin Bach]


## v0.3.1 (2017-02-11)

### Fixes

* Configurable logout redirect url via LOGINAS_LOGOUT_REDIRECT_URL (#49) [Aamir Adnan]

* Do not update user.last_login, overridable via LOGINAS_UPDATE_LAST_LOGIN (#48) [Aamir Adnan]


## v0.3.0 (2016-12-05)

### Features

* Add french translation (#43) [palmitoto]

### Fixes

* Rename MESSAGE_LOGIN_REVERT to LOGINAS_MESSAGE_LOGIN_REVERT. [Stavros Korokithakis]

* Ability set tags on messages and a minor compatibility fix (#47) [Aamir Adnan]

* Remove signer error logging (#45) [palmitoto]

* Remove user session flag on logout (#42) [palmitoto]


## v0.2.2 (2016-06-29)

### Fixes

* Support custom User models with customized username fields. (#36) [Ganesh Prasannah (GP)]


## v0.2.1 (2016-06-11)

### Fixes

* Fix login message for unicode username (#35) [Alex Riina]


## v0.2.0 (2016-06-01)

### Features

* After logging in as a user, restore to the previous user again when logging out. [Benjamin Bach]

### Fixes

* Escape early if a backend is not found. [Stavros Korokithakis]


## v0.1.10 (2016-05-30)

### Fixes

* Disallow logging in as superusers. [Stavros Korokithakis]


## v0.1.9 (2016-04-07)

### Fixes

* Remove pytest from setup.cfg. [Stavros Korokithakis]


## v0.1.8 (2016-04-07)

### Fixes

* Make loginas compatible with semantic-release. [Stavros Korokithakis]


