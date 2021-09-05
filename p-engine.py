from os import path
import hashlib
import hmac
import base64
from flask import (
    Flask,
    send_from_directory,
    render_template,
    request,
    jsonify,
    redirect,
)

import logzero
import config
from logzero import logger as log
from flask_login import LoginManager, UserMixin
from generator import searchPorn

logzero.json()

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.config.from_object(config)
app.secret_key = app.config["SECRET_KEY"]


def string_generator(data_incoming):
    data = data_incoming.copy()
    del data["hash"]
    keys = sorted(data.keys())
    string_arr = []
    for key in keys:
        string_arr.append(key + "=" + data[key])
    string_cat = "\n".join(string_arr)
    return string_cat


@app.route("/vidya")
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
def search_query(query):
    results = int(request.args.get("results", default=105))
    length = int(request.args.get("length", default=20))

    urls = searchPorn(query, results=results, length=length)

    def stream():
        return next(urls)

    return app.response_class(stream(), mimetype="text/plain")


@app.route("/login")
def login():
    tg_data = {
        "id": request.args.get("id", None),
        "first_name": request.args.get("first_name", None),
        "last_name": request.args.get("last_name", None),
        "username": request.args.get("username", None),
        "auth_date": request.args.get("auth_date", None),
        "hash": request.args.get("hash", None),
    }

    log.debug(tg_data)
    log.debug(app.config["BOT_TOKEN"])

    data_check_string = string_generator(tg_data)
    secret_key = hashlib.sha256(app.config["BOT_TOKEN"].encode("utf-8")).digest()
    secret_key_bytes = secret_key
    data_check_string_bytes = bytes(data_check_string, "utf-8")
    hmac_string = hmac.new(
        secret_key_bytes, data_check_string_bytes, hashlib.sha256
    ).hexdigest()
    if hmac_string == tg_data["hash"]:
        return redirect("/dashboard")

    return jsonify(
        {"hmac_string": hmac_string, "tg_hash": tg_data["hash"], "tg_data": tg_data}
    )


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")

#  vim: set ft=python sw=4 tw=0 fdm=manual et :
