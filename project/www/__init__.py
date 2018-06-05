from flask import Flask
from werkzeug.debug import DebuggedApplication
from project.db import make_www_session
import project.flask_config

app = Flask(__name__)
app.config.from_object(project.flask_config)
app.debug = True
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

db_session = make_www_session(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


import project.www.routes