from flask import *
from flask_session import Session
from websocket_server import WebsocketServer

import secrets

#  Website settings
HOST = "127.0.0.1"
WEB_PORT = 8080

#  Websocket settings
EXTERNAL_HOST = "127.0.0.1"
WEBSOCKET_PORT = 8081

#  Init
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

#  Creating secret key
SECRET_KEY = secrets.token_hex(16).encode('utf-8')
app.secret_key = SECRET_KEY
Session(app)

#  START -------------------------------------- WEB ---------------------------------------
@app.route('/')
def index():
    return render_template("main.html")

@app.route('/terms')
def terms():
    return render_template("terms.html")

@app.route('/chat', methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        if "country_code" in request.form:
            return render_template("chat.html", country_code=request.form["country_code"],
                                   websocket_host=EXTERNAL_HOST, websocket_port=WEBSOCKET_PORT,
                                   age=request.form["age"], sex=request.form["sex"])
    
    return render_template("main.html")

#  END    -------------------------------------- WEB ---------------------------------------

#  START -------------------------------------- API ---------------------------------------


#  END    -------------------------------------- API ---------------------------------------

#  Inject Variables
@app.context_processor
def inject_vars():
    return dict(project_name="ChatWave")
    

if __name__ == '__main__':
    ws = WebsocketServer(EXTERNAL_HOST, WEBSOCKET_PORT)
    ws.run_in_thread()

    app.run(host=HOST, port=WEB_PORT, debug=True, use_reloader=False)
    
    
