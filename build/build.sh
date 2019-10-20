#!/bin/bash

set -eo pipefail
shopt -s nullglob
cd $(dirname "$0")

echo "Building frontend"
(
    cd ../frontend
    npm run build
)

echo "Building backend"
(
    cd ../backend
    . .ve/bin/activate
    python setup.py sdist
)

echo "Create dist"
(
    cd ..
    rm -rf dist || True
    mkdir dist
    cp ./build/Dockerfile ./dist/
    cp ./build/gunicorn.config ./dist/
    cp ./backend/dist/web_backend-0.0.tar.gz ./dist
    cp ./build/keys.env ./dist
    cp ./build/run_server.sh ./dist
    cp -r ./backend/src/web_backend/front ./dist/front
    cp ./build/nginx.conf ./dist/
)

echo "Deploy..."
(
    cd ..
    tar -zcvf dist.tar.gz dist
    ./build/deploy.sh
)

echo "Done"