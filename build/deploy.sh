#!/bin/bash

cd $(dirname "$0")

source ./access.env

cd ../

SERVER=$USER@$IP



ssh -i $KEY $SERVER "rm -rf /home/$USER/dist.tar.gz /home/$USER/dist || True"
scp -i $KEY ./dist.tar.gz  $SERVER:/home/$USER/dist.tar.gz


ssh -i $KEY $SERVER 'tar -zxvf dist.tar.gz'

ssh -i $KEY $SERVER "cd /home/$USER/dist && docker build ./ --tag 'pubmed:0.1'"

ssh -i $KEY $SERVER 'docker stop pubmed'
ssh -i $KEY $SERVER 'docker container rm pubmed'
ssh -i $KEY $SERVER "docker run -d --restart always --name pubmed -p 80:8080 pubmed:0.1"