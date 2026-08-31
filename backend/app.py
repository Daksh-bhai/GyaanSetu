import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from flask import Flask
from flask_cors import CORS

from routes.auth_routes     import auth_bp
from routes.session_routes  import session_bp
from routes.test_routes     import test_bp
from routes.learning_routes import learning_bp
from routes.admin_routes    import admin_bp
from routes.report_routes   import report_bp

# ── SocketIO ──────────────────────────────────────────────────
from socket_events import init_socketio

app = Flask(__name__)
CORS(app, origins="*")

# Register blueprints
app.register_blueprint(auth_bp,     url_prefix="/api/auth")
app.register_blueprint(session_bp,  url_prefix="/api/sessions")
app.register_blueprint(test_bp,     url_prefix="/api/test")
app.register_blueprint(learning_bp, url_prefix="/api/learn")
app.register_blueprint(admin_bp,    url_prefix="/api/admin")
app.register_blueprint(report_bp,   url_prefix="/api/report")

# Initialize SocketIO
socketio = init_socketio(app)


@app.route("/")
def home():
    return {"message": "GyaanSetu Backend Running ✅"}


if __name__ == "__main__":
    # Must use socketio.run() instead of app.run()
    socketio.run(app, debug=True, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)