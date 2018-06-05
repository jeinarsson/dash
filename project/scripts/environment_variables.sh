
# Defaults - override in environment_variables_user.sh (not in git repo)
export DATABASE_URL='sqlite:///data/dash.db'


# Source user environment variables if they exist
F='./environment_variables_user.sh'
if [ -f $F ]; then
	echo 'Sourcing USER environment_variables_user.sh'
    . $F
fi
