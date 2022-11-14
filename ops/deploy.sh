#!/bin/bash
# script to deploy flask website with gunicorn and nginx (ubuntu22.04)

# create project folder
PROJECT="aiblogger"
#git clone -q https://github.com/BohdanBykov/$PROJECT.git /srv/$PROJECT/ \
#	&& echo "$PROJECT cloned into /srv/"

# install software
apt -y update \
	&& echo "apt repos updated"

apt install -y nginx python3 python3-pip python3-virtualenv mysql-server curl \
	&& echo "python, pip, venv, curl and nginx installed succesfully"

# prepare project folder
cd /srv/$PROJECT \
	&& echo "change directory to /srv/$PROJECT"

virtualenv env ; source env/bin/activate \
	&& echo "create and activate venv in /srv/$PROJECT"

pip install -r requirements.txt \
	&& echo "all requirements for $PROJECT installed"

# set up mysql server
systemctl start mysql.service && systemctl enable mysql.service \
	&& echo "started mysql server"

mysql -uroot -p mysql < /srv/aiblogger/ops/site_db_bcp.sql \
	&& echo "site_db imported"
mysql -uroot -p mysql < /srv/aiblogger/ops/mysql_bcp.sql \
	&& echo "mysql db imported"
systemctl restart mysql \
	&& echo "mysql daemon restarted"

# open db_config (user must imput values and save as db_conf.py)
nano /srv/$PROJECT/instance/tmpl_db_conf.py;

# add gunicorn service config
cp -f /srv/$PROJECT/ops/gunicorn.socket /etc/systemd/system/gunicorn.socket \
	&& echo "gunicorn socket copied to /etc/systemd/system"

cp -f /srv/$PROJECT/ops/gunicorn.service /etc/systemd/system/gunicorn.service \
	&& echo "gunicorn service copied to /etc/systemd/system"

# activate gunicorn
systemctl start gunicorn.socket ; systemctl enable gunicorn.socket \
	&& echo "gunicorn.socket started"

file /run/gunicorn.sock; curl --unix-socket /run/gunicorn.sock localhost \
	&& echo "test request to gunicorn socket sended"

# set up nginx
cp -f /srv/$PROJECT/ops/nginx.conf /etc/nginx/nginx.conf \
	&& echo "nginx config copied to /etc/nginx/"

nginx -s reload && curl localhost \
	&& echo "index of your site is above"



