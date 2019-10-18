#!/bin/bash

cd $(dirname "$0")

source ../build/keys.env

export FLASK_ENV=development
export FLASK_DEBUG=true

python ./src/web_backend/main.py