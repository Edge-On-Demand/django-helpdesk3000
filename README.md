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

Development
-----------

To run unittests across multiple Python versions, install:

    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get update
    sudo apt-get install python-dev python3-dev python3.3-minimal python3.3-dev python3.4-minimal python3.4-dev python3.5-minimal python3.5-dev python3.6 python3.6-dev

To run all [tests](http://tox.readthedocs.org/en/latest/):

    export TESTNAME=; tox

To run tests for a specific environment (e.g. Python 2.7 with Django 1.4):
    
    export TESTNAME=; tox -e py27-django111

To run a specific test:
    
    export TESTNAME=.TicketBasicsTestCase.test_helpdesk_submit; tox -e py27-django111

To run the [documentation server](http://www.mkdocs.org/#getting-started) locally:

    mkdocs serve -a :9999

To [deploy documentation](http://www.mkdocs.org/user-guide/deploying-your-docs/), run:

    mkdocs gh-deploy --clean

To build and deploy a versioned package to PyPI, verify [all unittests are passing](https://travis-ci.org/chrisspen/django-helpdesk3000), and then run:

    python setup.py sdist
    python setup.py sdist upload
