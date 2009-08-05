import os
from setuptools import setup

version = '0.1.0'

setup(
    name='django-activitystreams',
    version=version,
    description='Reusable application for generating activity streams',
    long_description=open('docs/overview.rst').read(),
    author='Nowell Strite',
    author_email='nowell@strite.org',
    url='http://github.com/nowells/django-activitystreams/',
    packages=['activitystreams'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        ],
    )
