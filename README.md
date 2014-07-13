healthcarefinder
================

Health Care Finder

## How to setup

    $ mkvirtualenv healthcarefinder
    $ pip install -r requirements.txt

## How to test

With the virtualenv do this (you should use the username for http://www.geonames.org):

    $ POSTCODE_USERNAME='username' python api.py

In another terminal:

    $ curl localhost:5000/1

And in your browser:

    localhost:5000
