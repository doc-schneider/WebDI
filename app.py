import dash
import pandas as pd
from datetime import datetime, timedelta
from dash import Dash, html, dcc
import bcrypt
from flask import session, send_file, request, redirect
from flask_session import Session
import os
import json
from pathlib import Path
from dotenv import load_dotenv
import mimetypes

from DataOperations.Photo import PhotoFactory
from Initialize.Initialize import session_init, init_tables
import config

config.environment_app = "AZURE"   # "AZURE"  # LOCAL
config.environment_storage = "AZURE"  # "AZURE"  # LOCAL

FAILED_LOGINS = {}
MAX_ATTEMPTS = 3
LOCK_TIME = timedelta(hours=24)

if config.environment_app == "LOCAL":
    # Only for testing
    load_dotenv()
    with open("resources/auth_hash.json", "r") as f:
        VALID_USERNAME_PASSWORD_PAIRS = json.load(f)
elif config.environment_app == "AZURE":
        VALID_USERNAME_PASSWORD_PAIRS = json.loads(os.environ["USERS_JSON"])

init_tables(config.environment_storage)

dash_app = Dash(__name__, use_pages=True)
app = dash_app.server

os.makedirs(os.path.join(os.getcwd(), 'sessions'), exist_ok=True)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'  # Use the filesystem for sessions
app.config['SESSION_FILE_DIR'] = os.path.join(os.getcwd(), 'sessions')  # Directory to store session files
app.config['SESSION_PERMANENT'] = False  # Sessions will expire when the browser is closed
app.config['SESSION_USE_SIGNER'] = True  # Sign session cookies for security
Session(app)
session_init(app)

if config.environment_app == "AZURE":
    @app.before_request
    def protect_dash():
        if request.path.startswith("/") and not request.path.startswith("/login"):
            if "user" not in session:
                return redirect("/login")

if config.environment_app == "AZURE":
    def is_locked(username):
        entry = FAILED_LOGINS.get(username)
        if not entry:
            return False
        locked_until = entry.get("locked_until")
        if locked_until and locked_until > datetime.utcnow():
            return True
        return False

    def register_failed_attempt(username):
        entry = FAILED_LOGINS.setdefault(
            username,
            {"count": 0, "locked_until": None}
        )
        entry["count"] += 1
        if entry["count"] >= MAX_ATTEMPTS:
            entry["locked_until"] = datetime.utcnow() + LOCK_TIME

    def reset_attempts(username):
        FAILED_LOGINS.pop(username, None)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            if is_locked(username):
                return "Account für 24 Stunden gesperrt", 403

            stored_hash = VALID_USERNAME_PASSWORD_PAIRS.get(username)
            if stored_hash and bcrypt.checkpw(
                password.encode("utf-8"),
                stored_hash.encode("utf-8")
            ):
                reset_attempts(username)
                session["user"] = username
                return redirect("/")

            register_failed_attempt(username)
            return "Login fehlgeschlagen", 401

        return """
        <form method="post">
          <input name="username" placeholder="Username">
          <input name="password" type="password" placeholder="Password">
          <button type="submit">Login</button>
        </form>
        """

# TODO Into  some dedicated Blueprint module? Or Photo?
@app.route("/video")
def stream_video():
    # TODO Common call, decoding in PhotoFactory
    if config.environment_storage == "LOCAL":
        name = request.args.get("name")
        stream = Path(name)
        mimetype, _ = mimetypes.guess_type(name)
    elif config.environment_storage == "AZURE":
        # TODO No longer used, remove
        container = request.args.get("container")
        blob = request.args.get("blob")
        stream = PhotoFactory.stream_image(
            pd.Series(data={'AZURE_CONTAINER': container, 'AZURE_BLOB': blob}, index=['AZURE_CONTAINER', 'AZURE_BLOB']),
            config.environment_storage, config.environment_app
        )
        mimetype, _ = mimetypes.guess_type(blob)
    if not mimetype:
        mimetype = "application/octet-stream"  # fallback
    return send_file(stream, mimetype=mimetype)

# import json
# import zipfile
#
# with zipfile.ZipFile("assets/stickers/2026-03-07 18 13 12 - Konstanze Walther - b86d2f6e-b795-40de-82dd-eaf0523437c2.was") as z:
#     lottie_json = json.loads(z.read("animation/animation.json"))
#
# dcc.Store(
#     id="lottie-data",
#     data={
#         "wave": wave_json,
#         "smile": smile_json,
#         "dance": dance_json,
#     }
# )
#
# dcc.Store(
#     id="lottie-data",
#     data=lottie_json
# ),

dash_app.layout = html.Div([
    dcc.Location(id="url-redirect"),
    html.Div(
        [
            html.Div(html.B("Links zu Seiten")),
            html.Br()
        ] + [
            html.Div(
                dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
            ) for page in dash.page_registry.values()
        ] + [
            html.Hr()
        ]
    ),
    dash.page_container,
])

import Views.Callbacks

if __name__ == '__main__':
    if config.environment_app == "LOCAL":
        # dash_app.run(host='0.0.0.0', port=5000, debug=False)
        dash_app.run(host='192.168.0.225', port=5000, debug=False)
    elif config.environment_app == "AZURE":
        dash_app.run(debug=False)





