# aiblogger
***
## Description

This must be a news website, with articles generated automatically by machine learning from real news. Maybe I will implement it in future, but now I use it as my pet project to try different DevOps tools and methods.

Below you will find blocks about deploy and configuration of this project:
- Technology stack
- Instruction to deploy
- App structure
- Flask
	 - Generate response
	 - Connect to database
	 - Contain configuration
- Nginx and gunicorn
- Docker compose
- Ansible playbooks
- CI/CD with Jenkins
- Monitoring Prometheus+Grafana

***
## Technology stack

- **Framework:** Flask (Python) </br>
	I decided to use Flask instead of Django, because I don't have a purpose to create something complex and big, I just need a few pages and functions. In this view Flask looks more suitably.

- **Database**: MySQL </br>
	 The most popular free relational database, I think it is a classic decision. At minimum this site will contain articles with header and body, to identify them i will use id's.

- **Webserver**: gunicorn + Nginx </br>
	 This combination is offered in Flask documentation. 
	 Gunicorn is one of the most popular wsgi for python applications.
	 Nginx is fast and simple decision to implement reverse proxy for gunicorn, Apache is overpowered for my case.

- **Source control**: GitHub </br>
	 I think explanation isn't required)

- **CI/CD**: Jenkins </br>
	 Popular free tool, have a lot of modules and use cases.

- **Deploy**: Ansible </br>
	 Simple in use, python based and agentless, also very popular.

- **Build**: Docker </br>
	 In my case I do not have a lot of services to deploy and I can deploy them directly on host. But anyway i want to explore my knowledge of docker so why not?)

- **Host**: AWS 
	 I  want to work with AWS and I will test my project on AWS EC2 and RDS to make it ready to deploy on them.

***
## Instruction to deploy

1) Get a linux server (ubuntu22.04). 
	I use ubuntu22.04 because it is popular and available to install on EC2.
2) Make sure you can connect to the server from your machine via ssh. 
3) Install ansible on your machine(not server) 
	 Or if you are planning to use Jenkins install ansible on Jenkins server.
4) Configure ansible 
	- make sure that 'host_key_checking = False' in /etc/ansible/ansible.cfg.
	- edit /etc/ansible/hosts in that way:
	```
	# name of group of servers in [], and ip address or domain name below it
	[vm]
	111.111.111.111

	# variables that ansible will use for this group
	[vm:vars]
	ansible_user=serveruser
	ansible_password=userpassword
	ansible_sudo_pass=userpassword
	
	# environment variables for use in docker deploy
	mysql_host = 'mysql_db_address'
	mysql_pass = 'password_for_siteuser'
	secret_key = 'secret_key_for_flask'
	```
5) Clone aiblogger repo to machine with ansible 
6) Use command 'ansible-playblook aiblogger/ops/ansible_playbooks/docker_deploy_aws'
	Aws playbook connects to remote MySQL using address and pass from env vars (hosts).
	Dev playbook connected to MySQL started in docker compose.  
7) Last stage of the ansible playbook is a response from aiblogger site. 
8) If you want to set up Jenkins for CI/CD, search for instructions below.

***
## App structure

- ### Project tree:
```
aiblogger
├── config.py
├── Dockerfile
├── flaskr
│   ├── auth.py
│   ├── blog.py
│   ├── db.py
│   ├── __init__.py
│   ├── schema.sql
│   ├── static
│   │   └── style.css
│   └── templates
│       ├── auth
│       │   ├── login.html
│       │   └── register.html
│       ├── base.html
│       └── blog
│           ├── create.html
│           ├── index.html
│           └── update.html
├── ops
│   ├── ansible_playbooks
│   │   ├── docker_deploy_aws.yaml
│   │   ├── docker_deploy_dev.yaml
│   │   ├── docker_update_aws.yaml
│   │   ├── docker_update_dev.yaml
│   │   ├── host_deploy_dev.yaml
│   │   └── [out_of_work]-host_deploy.sh
│   ├── configs
│   │   ├── docker_nginx.conf
│   │   ├── gunicorn.service
│   │   ├── gunicorn.socket
│   │   └── host_nginx.conf
│   ├── docker-compose.yaml
│   └── Jenkinsfile
├── README.md
├── requirements.txt
└── wsgi.py

```

- ### config.py
	 file that contain configuration for flask app, and mysql connection

- ### flaskr 
	 Directory that contains all files that Flask framework need to operate html requests.
	- \_\_init\_\_.py - file where we define our application (engine).
	- auth.py - code that defines functions of register and authentication.
	- blog.py - code that builds the main page with articles.
	- db.py - code which define functions to connect and initialize mysql.
	- static - directory that contain css properties
	- templates - directory that contain html templates for every page.
		base.html - define header that we use for every page

- ### Dockerfile
	File with instructions to build flask application for docker

- ### ops
	Directory that contains configurations and playbooks to deploy.
	- ansible_playbooks - dir that store ansible playbooks
		host_deploy.sh bash script to deploy aiblogger without docker, but i didn't update it after adding new functionality( it won't work )
	- configs - dir that store nginx and gunicorn configs
		 You need gunicorn as a service only if you deploy aiblogger without docker.
		 If you deploy without docker, nginx will redirect requests to gunicorn socket.
	- docker-compose.yaml - file that describes what containers docker will start.
	- Jenkinsfile - file that contains instruction that Jenkins use to automatically deliver source code changes to remote server.

- ### README.md
	This file))

- ### requirements.txt
	File that contains a list of modules python need to start aiblogger.

- ### wsgi.py 
	File that contain instructions flask need to work with gunicorn.

***
## To be continued))...

