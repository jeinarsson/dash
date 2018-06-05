#!/bin/sh

. ./environment_variables.sh

echo 'STARTING GUNICORN SERVER.'
echo '-------------------------'
echo 'DATABASE_URL:' $DATABASE_URL

cd ../../
gunicorn -w 2 -b :8000 --max-requests 1 --reload project.www:app