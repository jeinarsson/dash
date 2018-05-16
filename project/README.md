# Flask / SQLAlchemy app template

## WWW

 - Flask app
 - gunicorn server starts project.www:app
 - flask config values in flask_config.py
 - app depends on environment variables for database url and other secrets

## Requirements

 - structured by common.txt (always needed), and those specific for development (dev.txt) or production (prod.txt)