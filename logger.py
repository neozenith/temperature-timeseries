import os, sys
import sqlite3
import datetime
import time
import logging
import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

log = logging.getLogger(__name__)
logging.basicConfig(filename="output.log", level=logging.INFO)


def main():
    log.info("Starting up...")
    db = setup_database("data.db")
    while True:
        log.info("read...")
        measure_wait(db, delay=5)


def setup_database(filepath):
    conn = sqlite3.connect(filepath)
    with open("schema.sql", "r") as s:
        schema = s.read()
    conn.execute(schema)
    conn.commit()
    return conn


def measure_wait(db, delay=2):
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        log.info(f"{now} {temperature}, {humidity}")
        persist_metric(f, now, "temperature", temperature)
        persist_metric(f, now, "humidity", humidity)
    else:
        log.warn("Failed to retrieve data from humidity sensor")

    time.sleep(delay)


def persist_metric(db, now, metric, value):
    now_iso = now.isoformat()
    now_ts = now.timestamp()
    db.execute(f'''
    INSERT INTO metrics () VALUES;
               ''')
    db.commit()


if __name__ == "__main__":
    main()
