#!/bin/bash

cd $(dirname "$0")

source ./access.env

cd ../

SERVER=$USER@$IP

NETWORK=pubmeta


ssh -i $KEY $SERVER << EOF
 docker stop ingress
 docker stop pubmed

 docker container rm ingress
 docker container rm pubmed

 docker network rm $NETWORK

 rm -rf /home/$USER/dist.tar.gz
 rm -rf /home/$USER/dist
EOF

scp -i $KEY ./dist.tar.gz  $SERVER:/home/$USER/dist.tar.gz

NGINX_CFG="type=bind,source=/home/$USER/dist/nginx.conf,target=/etc/nginx/conf.d/default.conf"
NGINX_FRONT="/home/$USER/dist/front:/front"

ssh -i $KEY $SERVER << EOF
cd cd /home/$USER/
tar -zxvf dist.tar.gz

cd /home/$USER/dist 

docker build ./ --tag pubmed:0.1

docker network create $NETWORK

docker run -d --restart always --name pubmed   --net $NETWORK  pubmed:0.1

docker run -d --restart always --name ingress  --net $NETWORK  -p 80:80 -p 443:443 --mount $NGINX_CFG -v $NGINX_FRONT -v /etc/letsencrypt:/etc/letsencrypt nginx:latest
EOF