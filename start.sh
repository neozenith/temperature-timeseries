#! /bin/bash

. ./.venv/bin/activate
pip install -r .deps/requirements-dev.txt

if [ -z "$(ps aux | grep logger.py | grep -v grep)" ]; then
  python3 logger.py &
else
  echo "Already running logger.py"
fi

if [ -z "$(ps aux | grep gunicorn | grep -v grep)" ]; then
  gunicorn -w 4 -b 0.0.0.0:8000 server:app &
else 
  echo "Already running server.py"
fi
