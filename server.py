from flask import Flask, render_template
from flask import current_app, g
import sqlite3
import logging

log = logging.getLogger(__name__)

app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("data.db", detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


@app.route("/")
def index():
    output = "<html><body>"
    for stat in stats():
        for s in stat:
            output += f"<div>{s}</div>"
    output += "</body></html>"
    return output


def stats():
    conn = get_db()
    results = conn.execute("SELECT count(*), max(ts_iso8601) FROM metrics;")
    return [r for r in results]


if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0")
