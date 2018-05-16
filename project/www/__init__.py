from flask import Flask
from werkzeug.debug import DebuggedApplication
import project.flask_config

app = Flask(__name__)
app.config.from_object(project.flask_config)
app.debug = True
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

# read dash config json here

@app.teardown_appcontext
def shutdown_session(exception=None):
    pass

import project.www.routes