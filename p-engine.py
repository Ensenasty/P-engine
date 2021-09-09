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

from generator import searchPorn

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.route("/")
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

    #  [print(u) for u in urls]


# @app.route("/logout")
# @login_required
# def logout():
#     User.logout()
#     return redirect("/")


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")

#  vim: set ft=python sw=4 tw=0 fdm=manual et :
