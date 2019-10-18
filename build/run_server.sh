#!/bin/bash

source /keys.env

exec gunicorn --config /gunicorn.config web_backend:app