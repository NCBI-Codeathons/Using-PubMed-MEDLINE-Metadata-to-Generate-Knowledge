#!/bin/bash

cd $(dirname "$0")

export FLASK_ENV=development
export FLASK_DEBUG=true

python ./src/web_backend/main.py