import os
import sys
from distutils.util import convert_path
from fnmatch import fnmatchcase
from setuptools import setup, find_packages, Command

import helpdesk

# Provided as an attribute, so you can append to these instead
# of replicating them:
standard_exclude = ('*.py', '*.pyc', '*$py.class', '*~', '.*', '*.bak')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build',
                                './dist', 'EGG-INFO', '*.egg-info')

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    #sudo apt-get install pandoc
    #sudo pip install pyandoc
    read_md = lambda f: open(f, 'r').read()

def get_reqs(test=False):
    # optparse is included with Python <= 2.7, but has been deprecated in favor
    # of argparse.  We try to import argparse and if we can't, then we'll add
    # it to the requirements
    reqs = [
        'Django>=1.4.0',
        #'python-dateutil>=2.2',
        #'psutil>=2.1.1',
        'six>=1.7.2',
    ]
    if test:
        reqs.append('South>=0.8.4')
    return reqs

# (c) 2005 Ian Bicking and contributors; written for Paste (http://pythonpaste.org)
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
# Note: you may want to copy this into your setup.py file verbatim, as
# you can't import this from another package, when you don't know if
# that package is installed yet.
def find_package_data(
    where='.', package='',
    exclude=standard_exclude,
    exclude_directories=standard_exclude_directories,
    only_in_packages=True,
    show_ignored=False):
    """
    Return a dictionary suitable for use in ``package_data``
    in a distutils ``setup.py`` file.

    The dictionary looks like::

        {'package': [files]}

    Where ``files`` is a list of all the files in that package that
    don't match anything in ``exclude``.

    If ``only_in_packages`` is true, then top-level directories that
    are not packages won't be included (but directories under packages
    will).

    Directories matching any pattern in ``exclude_directories`` will
    be ignored; by default directories with leading ``.``, ``CVS``,
    and ``_darcs`` will be ignored.

    If ``show_ignored`` is true, then all the files that aren't
    included in package data are shown on stderr (for debugging
    purposes).

    Note patterns use wildcards, or can be exact paths (including
    leading ``./``), and all searching is case-insensitive.
    """

    out = {}
    stack = [(convert_path(where), '', package, only_in_packages)]
    while stack:
        where, prefix, package, only_in_packages = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        if show_ignored:
                            print >> sys.stderr, (
                                "Directory %s ignored by pattern %s"
                                % (fn, pattern))
                        break
                if bad_name:
                    continue
                if (os.path.isfile(os.path.join(fn, '__init__.py'))
                    and not prefix):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                    stack.append((fn, '', new_package, False))
                else:
                    stack.append((fn, prefix + name + '/', package, only_in_packages))
            elif package or not only_in_packages:
                # is a file
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        if show_ignored:
                            print >> sys.stderr, (
                                "File %s ignored by pattern %s"
                                % (fn, pattern))
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out

class TestCommand(Command):
    description = "Runs unittests."
    user_options = [
        ('name=', None,
         'Name of the specific test to run.'),
        ('virtual-env-dir=', None,
         'The location of the virtual environment to use.'),
        ('pv=', None,
         'The version of Python to use. e.g. 2.7 or 3'),
    ]
    
    def initialize_options(self):
        self.name = None
        self.virtual_env_dir = './.env%s'
        self.pv = 0
        self.versions = [2.7]#, 3]#TODO:support Python3
        
    def finalize_options(self):
        pass
    
    def build_virtualenv(self, pv):
        virtual_env_dir = self.virtual_env_dir % pv
        kwargs = dict(virtual_env_dir=virtual_env_dir, pv=pv)
        if not os.path.isdir(virtual_env_dir):
            cmd = 'virtualenv -p /usr/bin/python{pv} {virtual_env_dir}'.format(**kwargs)
            #print(cmd)
            os.system(cmd)
            
            cmd = '. {virtual_env_dir}/bin/activate; easy_install -U distribute; deactivate'.format(**kwargs)
            os.system(cmd)
            
            for package in get_reqs(test=True):
                kwargs['package'] = package
                cmd = '. {virtual_env_dir}/bin/activate; pip install -U {package}; deactivate'.format(**kwargs)
                #print(cmd)
                os.system(cmd)
    
    def run(self):
        versions = self.versions
        if self.pv:
            versions = [self.pv]
        
        for pv in versions:
            
            self.build_virtualenv(pv)
            kwargs = dict(pv=pv, name=self.name)
                
            if self.name:
                cmd = '. ./.env{pv}/bin/activate; django-admin.py test --pythonpath=. --traceback --settings=helpdesk.tests.settings helpdesk.tests.tests.{name}; deactivate'.format(**kwargs)
            else:
                cmd = '. ./.env{pv}/bin/activate; django-admin.py test --pythonpath=. --traceback --settings=helpdesk.tests.settings helpdesk.tests; deactivate'.format(**kwargs)
                
            print(cmd)
            ret = os.system(cmd)
            if ret:
                return

class PEP8Command(Command):
    description = "Checks code formatting."
    user_options = [
    ]
    
    def initialize_options(self):
        pass
        
    def finalize_options(self):
        pass
    
    def run(self):
        cmd = 'pylint --rcfile=pylint.rc helpdesk'
        os.system(cmd)


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
        "Topic :: Software Development :: Bug Tracking",
    ],
    keywords=['django', 'helpdesk', 'tickets', 'incidents', 'cases'],
    author='Chris Spencer',
    author_email='chrisspen@gmail.com',
    url='https://github.com/chrisspen/django-helpdesk3000',
    license='BSD',
    packages=find_packages(),
    package_data=find_package_data("helpdesk", only_in_packages=False),
    include_package_data=True,
    zip_safe=False,
    install_requires=get_reqs(),
    cmdclass={
        'test': TestCommand,
        'pep8': PEP8Command,
    },
)

