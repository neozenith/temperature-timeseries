# Timeseries Analysis

# Setup

https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/

```bash
python3 -m venv .venv
. ./venv/bin/activate
pip install -r .deps/requirements-dev.txt
python3 logger.py &
python3 server.py &
```

# Data

Data is saved to a SQLite3 database on the RPi using the schema in `schema.sql`

# Analysis

With a simple set of timeseries measurements of temperature in my study can I apply
each of the libraries below?

 - https://tslearn.readthedocs.io/en/latest/
 - https://facebook.github.io/prophet/docs/quick_start.html

# TODO
 - Explore analysis tools
 - Use Plotly to generate visuals
 - Use plotly to create live dashboards
 - Centralise data by pushing to the cloud.
 - Handle caching offline and forwarding once delivered.
 - Setup Heroku instance to visualise from cloud.
