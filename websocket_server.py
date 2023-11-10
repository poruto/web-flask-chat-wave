from flask import *
from flask_session import Session

import secrets

#  Settings
HOST = "127.0.0.1"
WEB_PORT = 8080

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
    if request.method == "GET":
        return render_template("main.html")
    elif request.method == "POST":
        return render_template("chat.html")

#  END    -------------------------------------- WEB ---------------------------------------

#  START -------------------------------------- API ---------------------------------------


#  END    -------------------------------------- API ---------------------------------------

#  Inject Variables
@app.context_processor
def inject_vars():
    return dict(project_name="ChatWave")
    

if __name__ == '__main__':
    app.run(host=HOST, port=WEB_PORT, debug=True, use_reloader=True)
    
    
