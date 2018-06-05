#!/bin/sh

cd ~/git/dash/project/scripts
. ./environment_variables.sh

echo 'Running Mail reminders.'
echo '----------------------'

cd $DASH_HOME
export PYTHONPATH=$DASH_HOME
python project/tasks/send_mail_reminders.py
