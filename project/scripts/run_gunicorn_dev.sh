#!/bin/sh

. ./environment_variables.sh

echo 'STARTING GUNICORN SERVER.'
echo '-------------------------'
echo 'DASH_HOME:' $DASH_HOME
echo 'DATABASE_URL:' $DATABASE_URL
echo 'Running as '$(whoami)

cd $DASH_HOME
gunicorn -w 2 -b :8000 --max-requests 1 --reload project.www:app