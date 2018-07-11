from __future__ import print_function

import os
from pprint import pprint

from setuptools import setup, find_packages

import helpdesk

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


def get_reqs(*fns):
    lst = []
    for fn in fns:
        for package in open(os.path.join(CURRENT_DIR, fn)).readlines():
            package = package.strip()
            if not package:
                continue
            lst.append(package.strip())
    return lst


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk('helpdesk/'+directory):
        for filename in filenames:
            paths.append(os.path.join(path.replace('helpdesk/', ''), filename))
    return paths


extra_files = []
extra_files.extend(package_files('fixtures'))
extra_files.extend(package_files('locale'))
extra_files.extend(package_files('static'))
extra_files.extend(package_files('templates'))
extra_files.extend(package_files('tests/fixtures'))
pprint(extra_files, indent=4)

setup(
    name='django-helpdesk3000',
    version=helpdesk.__version__,
    description="Django-powered ticket tracker for your helpdesk",
    long_description=read_md('README.md'),
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Intended Audience :: Customer Service",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Topic :: Office/Business",
        "Topic :: Software Development :: Bug Tracking"
    ],
    keywords=['django', 'helpdesk', 'tickets', 'incidents', 'cases'],
    author='Chris Spencer',
    author_email='chrisspen@gmail.com',
    url='https://github.com/chrisspen/django-helpdesk3000',
    license='BSD',
    packages=find_packages(),
    package_data={
        '': ['docs/*'],
        'helpdesk': extra_files
    },
    zip_safe=False,
    install_requires=get_reqs('requirements-min-django.txt', 'requirements.txt')
)
