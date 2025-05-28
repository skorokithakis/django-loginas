# Changelog


## Unreleased

### Features

* Add the Persian translation files (#106) [Mahdi Namaki]

* Redirect logouts to the 'next' url (#100) [Rodolfo Torres]

* Remove six and Py2 support. [Stavros Korokithakis]

* Change changelog format to Markdown. [Stavros Korokithakis]

* Drop Python 2 support. [Stavros Korokithakis]

* Customize username field through settings.py (#72) [Eric Goddard]

* Add french translation (#43) [palmitoto]

* After logging in as a user, restore to the previous user again when logging out. [Benjamin Bach]

### Fixes

* Mention another alternative for the loginas button when using a custom user model (#109) [Matthias Kestenholz]

* Add .po and .mo files to the manifest. [Stavros Korokithakis]

* Updates for Python 3.10 and Django 4.0 (#99) [Tom Carrick]

* Modernize Django URL's (#93) [Adam Johnson]

* Don't crash when session doesn't exist (#86) [Gady Pitaru]

* Catch ImproperlyConfigured exc in user_login view (#85) [Sergei Zherevchuk]

* Add PermissionDenied support for `can_login_as` (#84) [Sergei Zherevchuk]

* Don't require the messages framework (#80) [Jerome Leclanche]

* Constrain admin button to User model (#74) [Steve Kossouho]

* Skip backends that don't have a `get_user` method (#69) [Berk Birand]

* Add 0.3.1 to changelog (#56) [Benjamin Bach]

* Configurable logout redirect url via LOGINAS_LOGOUT_REDIRECT_URL (#49) [Aamir Adnan]

* Do not update user.last_login, overridable via LOGINAS_UPDATE_LAST_LOGIN (#48) [Aamir Adnan]

* Rename MESSAGE_LOGIN_REVERT to LOGINAS_MESSAGE_LOGIN_REVERT. [Stavros Korokithakis]

* Ability set tags on messages and a minor compatibility fix (#47) [Aamir Adnan]

* Remove signer error logging (#45) [palmitoto]

* Remove user session flag on logout (#42) [palmitoto]

* Support custom User models with customized username fields. (#36) [Ganesh Prasannah (GP)]

* Fix login message for unicode username (#35) [Alex Riina]

* Escape early if a backend is not found. [Stavros Korokithakis]

* Disallow logging in as superusers. [Stavros Korokithakis]

* Remove pytest from setup.cfg. [Stavros Korokithakis]

* Make loginas compatible with semantic-release. [Stavros Korokithakis]


