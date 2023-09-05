#!/bin/sh

KDIR="${HOME}/klipper"
KENV="${HOME}/klippy-env"

DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

if [ ! -d "$KDIR" ] || [ ! -d "$KENV" ]; then
    echo "smartplug: klipper or klippy env doesn't exist"
    exit 1
fi

# install smartplug requirements to env
echo "smartplug: installing python requirements to env."
"${KENV}/bin/pip" install -r "${DIR}/requirements.txt"

# update link to smartplug.py
echo "smartplug: linking klippy to smartplug.py."
if [ -e "${KDIR}/klippy/extras/smartplug.py" ]; then
    rm "${KDIR}/klippy/extras/smartplug.py"
fi
ln -s "${DIR}/smartplug.py" "${KDIR}/klippy/extras/smartplug.py"

# exclude smartplug.py from klipper git tracking
if ! grep -q "klippy/extras/smartplug.py" "${KDIR}/.git/info/exclude"; then
    echo "klippy/extras/smartplug.py" >> "${KDIR}/.git/info/exclude"
fi
echo "smartplug: installation successful."
