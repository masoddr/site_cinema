#!/bin/bash
export FLASK_APP=wsgi.py
export FLASK_ENV=development
export FLASK_DEBUG=1

flask run --host=0.0.0.0 --port=5000 