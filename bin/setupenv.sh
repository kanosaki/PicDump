#!/bin/bash

function missing() {
    which $1 > /dev/null 2>&1
    (( $? != 0 ))
}

BINDIR=$(dirname $0)
PIP_REQUIREMENTS=$BINDIR/../requirements.txt

if (( UID != 0 )); then
    echo "WARNING: This script may require root privilege."
fi


if missing pip; then
    echo "Installing pip"
    easy_install pip
fi

pip install -r $PIP_REQUIREMENTS
