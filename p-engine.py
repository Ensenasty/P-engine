from os import path
from flask import Flask, send_from_directory, render_template, request
from bingporn import get_direct_link

from google.cloud.logging.handlers import setup_logging
from google.cloud.logging.handlers import CloudLoggingHandler


client = google.cloud.logging.Client()
handler = CloudLoggingHandler(client)
logging.getLogger().setLevel(logging.DEBUG)  # defaults to WARN
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=loggng.INFO
)
cloudlogs = setup_logging(handler)

from logzero import setup_logger

log = setup_logger(
    name=cloudlogs, logfile=None, isRootLogger=True, json=True, json_esure_ascii=True
)
log.warning("Native Cloud Logging now enabled.")

import sys
from google.cloud import error_reporting

erc = error_reporting.Client(project="mezaops", service="bingporn", version="0")


def custom_excepthook(exctype, value, traceback):
    user = "ay@no-ma.me"
    errstr = exctype.str()
    erc.report()
    sys.__excepthook__(exctype, value, traceback)


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
def direct_vid_link(query):
    results = int(request.args.get("results", default=105))
    length = int(request.args.get("length", default=20))
    direct_link = get_direct_link(query, results=results, length=length)
    return direct_link


if __name__ == "__main__":
    import os
    import sys

    PORT = sys.argv[1] if len(sys.argv) > 1 else "6969"
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


#  vim: set ft=python sw=4 tw=0 fdm=manual et :
