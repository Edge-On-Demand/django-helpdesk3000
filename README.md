django-helpdesk3000 - A Django powered ticket tracker.
======================================================

This is a Django-powered helpdesk ticket tracker, designed to
plug into an existing Django website and provide you with 
internal (or, perhaps, external) helpdesk management.

It's a fork of [django-helpdesk](https://github.com/rossp/django-helpdesk)
with better styling, more features, and numerous bug fixes.

Installation
------------

Install via pip with:

    pip install django-helpdesk3000

Then add `helpdesk` to the `INSTALLED_APPS` list in your `settings.py`.

Then apply the models. If you're using South, simply run:

    python manage.py migrate helpdesk

or if not using South:

    python manage.py syncdb

For further installation information see docs/install.html and docs/configuration.html
