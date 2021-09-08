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

from flask_login import LoginManager, UserMixin
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

<<<<<<< HEAD
    return app.response_class(stream(), mimetype="text/plain")
=======
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

    if tg_data["id"] and is_valid(tg_data):
        user = User(tg_data)
        return user 
    else:
        return None

# @app.route("/logout")
# @login_required
# def logout():
#     User.logout()
#     return redirect("/")
>>>>>>> cdcfd68... Upgraded bootstrap


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")

#  vim: set ft=python sw=4 tw=0 fdm=manual et :
