#! /bin/bash
date
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
START_DIR="$(pwd)"

echo -e "SCRIPT DIR: ${SCRIPT_DIR}"
echo -e "START DIR: ${START_DIR}"

cd $SCRIPT_DIR
date
source .venv/bin/activate
pip install -r .deps/requirements.txt
date
if [ -z "$(ps u | grep logger.py | grep -v grep)" ]; then
  python3 logger.py &
else
  echo "Already running logger.py"
fi

