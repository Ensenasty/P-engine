from os import path
import base64

import hashlib
import hmac
from flask import (
    Flask,
    send_from_directory,
    render_template,
    request,
    jsonify,
    redirect,
)

from flask_login.utils import login_required
from urllib.parse import urlparse, urljoin

import logzero
from logzero import logger as log

logzero.json()

import config
from generator import searchPorn
from userclass import User

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.config.from_object(config)
app.secret_key = app.config["SECRET_KEY"]

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"
login_manager.login_message = "Para ver esta página debes ser miembro de Ensenasty club"
login_manager.login_message_category = "info"


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def string_generator(data_incoming):
    data = data_incoming.copy()
    del data["hash"]
    keys = sorted(data.keys())
    string_arr = []
    for key in keys:
        string_arr.append(key + "=" + data[key])
    string_cat = "\n".join(string_arr)
    return string_cat

def is_valid(tg_data):
    data_check_string = string_generator(tg_data)
    secret_key = hashlib.sha256(app.config["BOT_TOKEN"].encode("utf-8")).digest()
    secret_key_bytes = secret_key
    data_check_string_bytes = bytes(data_check_string, "utf-8")
    hmac_string = hmac.new(
        secret_key_bytes, data_check_string_bytes, hashlib.sha256
    ).hexdigest()
    return hmac_string == tg_data["hash"]
        


@app.route("/auth")
def register_auth():
    pass


@app.route("/firehose")
@login_required
def main_page():
    cols = int(request.args.get("cols", default=2))
    rows = int(request.args.get("rows", default=2))
    results = int(request.args.get("results", default=105))
    length = int(request.args.get("length", default=20))
    search = request.args.get("search", default="default")
    return render_template(
        "vid_grid.html",
        cols=cols,
        rows=rows,
        results=results,
        length=length,
        search=search,
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/search/<query>")
@login_required
def search_query(query):
    results = int(request.args.get("results", default=105))
    length = int(request.args.get("length", default=20))

    urls = searchPorn(query, results=results, length=length)

    def stream():
        return next(urls)

    return app.response_class(stream(), mimetype="text/plain")


@login_manager.request_loader
def load_user_from_request(request):
    tg_data = {
        "id": request.args.get("id", None),
        "first_name": request.args.get("first_name", None),
        "last_name": request.args.get("last_name", None),
        "username": request.args.get("username", None),
        "auth_date": request.args.get("auth_date", None),
        "hash": request.args.get("hash", None),
        "photo_url": request.args.get("photo_url", None)
    }

    log.debug(tg_data)
    log.debug(app.config["BOT_TOKEN"])
    log.debug(app.config["SECRET_KEY"])

    if tg_data["id"]:
        if is_valid(tg_data):
            try:
                user = User(tg_data)
            except TypeError:
                return None
            return user 
        else:
            return None
    else:
        return None

    # return jsonify(
    #     {"hmac_string": hmac_string, "tg_hash": tg_data["hash"], "tg_data": tg_data}
    # )


# @app.route("/logout")
# @login_required
# def logout():
#     User.logout()
#     return redirect("/")


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")

#  vim: set ft=python sw=4 tw=0 fdm=manual et :
