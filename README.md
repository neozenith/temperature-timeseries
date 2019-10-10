# Timeseries Analysis

# Setup

[PiMyLifeup: DHT22](https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/)

```bash
. ./start.sh
```

# Data

Data is saved to a SQLite3 database on the RPi using the schema in `schema.sql`

# Analysis

Current export of the analysis notebook can be found at:

[Analysis](https://joshpeak.net/temperature-timeseries/analysis.html)

With a simple set of timeseries measurements of temperature in my study can I apply
each of the libraries below?

 - [tslearn](https://tslearn.readthedocs.io/en/latest/)
 - [Facebook's Prophet](https://facebook.github.io/prophet/docs/quick_start.html)

# TODO
 - Explore analysis tools
 - Centralise data by pushing to the cloud.
 - Handle caching offline and forwarding once delivered.
 - Setup Heroku instance to visualise from cloud.
