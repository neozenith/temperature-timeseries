import os, sys
import sqlite3
import datetime
import time
import logging
from influxdb import InfluxDBClient

log = logging.getLogger(__name__)
logging.basicConfig(filename="migrator.log", level=logging.INFO)

def influxdb_connection():
    return InfluxDBClient(database='metrics')


def sqlite_connection(filepath="data.db"):
    conn = sqlite3.connect(filepath)
    with open("schema.sql", "r") as s:
        schema = s.read()
    conn.executescript(schema)
    conn.commit()
    conn.row_factory = sqlite3.Row
    return conn


def main():
    log.info("Starting up...")
    sqlite_con = sqlite_connection()
    influxdb_con = influxdb_connection()
    for i in range(1000):
        rows = fetch(sqlite_con)
        log.info(f"Read {len(rows)} rows...")
        if len(rows) == 0:
            sys.exit(0)

        ids = persist_influxdb(influxdb_con, rows)
        mark_as_migrated(sqlite_con, ids)



def persist_influxdb(conn, rows):

    payload = [
        {
            "measurement": data['metric'],
            "tags": {
                "sensor_id": data['sensor_id'],
            },
            "time": datetime.datetime.fromtimestamp(data['ts'], tz=datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            "fields": {
                "value": data['value']
            }
        }
        for data in rows
    ]
    conn.write_points(payload)
    return [data['id'] for data in rows]


def fetch(conn):
    log.info(f"Fetching rows...")
    results = conn.execute(
        """
        SELECT
            id, sensor_id, metric, ts, value
        FROM
            metrics
        WHERE
            migrated IS NULL
        ORDER BY ts DESC
        LIMIT 10000
        """,
    )
    return [{k: r[k] for k in r.keys()} for r in results]

def mark_as_migrated(conn, ids):
    log.info(f"Mark {len(ids)} rows marked as done... ")
    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    now_ts = now.timestamp()
    conn.executemany(
        f"""UPDATE metrics SET migrated = ? WHERE id = ?""",
        [(now_ts, row_id) for row_id in ids],
    )
    conn.commit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.exception(e)
