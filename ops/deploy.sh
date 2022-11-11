#!/bin/bash
# script to deploy flask website with gunicorn and nginx (ubuntu22.04)

# # create project folder
# git clone https://github.com/BohdanBykov/aiblogger.git /srv/aiblogger/

# install software
apt -y update
apt install -y nginx python3 python3-pip python3-virtualenv curl

# prepare project folder
cd /srv/aiblogger
virtualenv env
source env/bin/activate
pip install -r requirements.txt

# add gunicorn service config
mv -f /srv/aiblogger/ops/gunicorn.socket /etc/systemd/system/gunicorn.socket
mv -f /srv/aiblogger/ops/gunicorn.service /etc/systemd/system/gunicorn.service

# activate gunicorn
file /run/gunicorn.sock
curl --unix.socket /run/gunicorn.sock localhost

# set up nginx
mv -f /srv/aiblogger/ops/nginx.conf /etc/nginx/nginx.conf
nginx -s reload

# load website
echo "result:"
curl localhost

