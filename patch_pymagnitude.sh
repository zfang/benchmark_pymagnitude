#!/usr/bin/env bash

PATCH=pymagnitude.__init__.py.patch
ORIGINAL=`python -c "import pymagnitude; print(pymagnitude.__file__)"`
patch $ORIGINAL $PATCH $@
