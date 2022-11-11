#!/bin/bash
# script to deploy flask with gunicorn and nginx (ubuntu22.04)

# install software
apt -y update
apt apt install -y nginx python3 python3-pip python3-virtualenv curl

# create project folder
git clone https://github.com/BohdanBykov/aiblogger.git /srv/aiblogger/

cd /srv/aiblogger
virtualenv env
source env/bin/activate
pip install -r requiremenst.txt

# add gunicorn service config
mv -f /srv/aiblogger/ops/gunicorn.socket /etc/systemd/system/gunicorn.socket
mv -f /srv/aiblogger/ops/gunicorn.service /etc/systemd/system/gunicorn.service

# activate gunicorn
file /run/gunicorn.sock
curl --unix.socket /run/gunicorn.sock localhost

# set up nginx
mv -f /home/administrator/config/nginx.conf /etc/nginx/nginx.conf
nginx -s reload

