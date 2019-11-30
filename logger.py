import os, sys
import sqlite3
import datetime
import time
import logging
import json
import Adafruit_DHT
from influxdb import InfluxDBClient

SENSOR_ID = "RPI4-DHT22"
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

log = logging.getLogger(__name__)
logging.basicConfig(filename="output.log", level=logging.INFO)

def influxdb_connection():
    return InfluxDBClient(database='metrics')


def sqlite_connection(filepath="data.db"):
    conn = sqlite3.connect(filepath)
    with open("schema.sql", "r") as s:
        schema = s.read()
    conn.executescript(schema)
    conn.commit()
    return conn


def main():
    log.info("Starting up...")
    sqlite_con = sqlite_connection()
    influxdb_con = influxdb_connection()
    while True:
        log.info("read...")
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

        if humidity is not None and temperature is not None:
            now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
            log.info(f"{now} {temperature}, {humidity}")

            persist_sqlite(sqlite_con, now, "temperature", temperature)
            persist_sqlite(sqlite_con, now, "humidity", humidity)
            persist_influxdb(influxdb_con, now, "temperature", temperature)
            persist_influxdb(influxdb_con, now, "humidity", humidity)
        else:
            log.warn("Failed to retrieve data from humidity sensor")

        time.sleep(5)



def persist_influxdb(conn, now, metric, value):
    log.info(f"Write InfluxDB points... {metric}")
    payload = [
        {
            "measurement": metric,
            "tags": {
                "sensor_id": SENSOR_ID,
            },
            "time": now.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "fields": {
                "value": value
            }
        }
    ]
    conn.write_points(payload)


def persist_sqlite(conn, now, metric, value):
    log.info(f"Write SQLite points... {metric}")
    now_iso = now.isoformat()
    now_ts = now.timestamp()
    conn.execute(
        f"""
    INSERT INTO metrics
        (sensor_id, insert_ts, ts, ts_iso8601, metric, value, migrated)
    VALUES
        (?, ?, ?, ?, ?, ?, ?)
    """,
        (SENSOR_ID, now_ts, now_ts, now_iso, metric, value, now_ts),
    )
    conn.commit()

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            log.exception(e)
