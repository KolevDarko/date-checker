#!/bin/bash
NAME="Date-Checker"
DJANGODIR=/home/darko/date-checker/
SOCKFILE=/home/darko/date-checker/run/gunicorn.sock   # we will communicate using this unix socket
USER=darko                                      # The user to run as
GROUP=darko                                   # The group to run as
NUM_WORKERS=1                                   # How many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=datecheck.settings.production          # Which settings file should Django use
DJANGO_WSGI_MODULE=datecheck.wsgi                  # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /home/darko/.local/share/virtualenvs/date-checker-YC9MYCJG/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --bind=unix:$SOCKFILE
