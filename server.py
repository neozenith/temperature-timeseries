import sqlite3
import datetime
import time
import logging

from flask import Flask, request, g
from flask import jsonify

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
    return jsonify(stats())


@app.route("/metrics")
def metrics():
    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    start = request.args.get("from", default=None, type=int)
    end = request.args.get("to", default=None, type=int)

    if start is None:
        start = (now - datetime.timedelta(days=1)).timestamp()
    else:
        start = (now - datetime.timedelta(days=start)).timestamp()

    if end is None:
        end = now.timestamp()
    else:
        end = (now - datetime.timedelta(days=end)).timestamp()
    return jsonify(stats(metric=None, start=start, end=end))


@app.route("/metric/<string:metric>/")
def get_metric(metric):
    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    start = request.args.get("from", default=None, type=int)
    end = request.args.get("to", default=None, type=int)

    if start is None:
        start = (now - datetime.timedelta(days=1)).timestamp()
    else:
        start = (now - datetime.timedelta(days=start)).timestamp()

    if end is None:
        end = now.timestamp()
    else:
        end = (now - datetime.timedelta(days=end)).timestamp()

    return jsonify(stats(metric, start, end))


def stats(metric=None, start=None, end=None):
    conn = get_db()
    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    last_day = (now - datetime.timedelta(days=1)).timestamp()

    if metric is not None:
        results = conn.execute(
            """
            SELECT
                id, ts, metric, value
            FROM metrics
            WHERE metric = ? AND ts >= ? AND ts <= ?
            ORDER BY ts DESC;
            """,
            [metric, start, end],
        )
    elif start is not None and end is not None:
        results = conn.execute(
            """
            SELECT
                id, ts, metric, value
            FROM metrics
            WHERE ts >= ? AND ts <= ?
            ORDER BY ts DESC;
            """,
            [start, end],

        )
    else:
        results = conn.execute(
            """
            SELECT
                metric,
                count(*) as count,
                min(value) as value_min,
                avg(value) as value_avg,
                max(value) as value_max
            FROM metrics
            WHERE ts >= ?
            GROUP BY metric
            """,
            [last_day],

        )

    return [{k: r[k] for k in r.keys()} for r in results]


if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0")
