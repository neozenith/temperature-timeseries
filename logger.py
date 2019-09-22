import os, sys
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
    with open("humidity.csv", "a+") as f:
        if os.stat("humidity.csv").st_size == 0:
            f.write("Datetime,Temperature,Humidity\r\n")

        while True:
            log.info("read...")
            measure_wait(f, delay=5)
            f.flush()


def measure_wait(f, delay=2):
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        log.info(f"{now} {temperature}, {humidity}")
        f.write("{0},{1:0.1f},{2:0.1f}\r\n".format(now, temperature, humidity))
    else:
        log.warn("Failed to retrieve data from humidity sensor")

    time.sleep(delay)


if __name__ == "__main__":
    main()
