# aiblogger
***
## Description

This must be a news website, with articals generated automatically by machine learning from real news. Maybe i will implement in future, but now i use it as my pet project to try different DevOps tools and methods.

Below you will find blocks about deploy and configuration of this project:
- Technology stack
- Instruction to deploy
- App structure
- Flask
	 - Run application
	 - \_\_init.py\_\_ define app
	 - Connect to database
	 - Contain configuration
- Nginx and gunicorn
- Docker compose
- Ansible playbooks
- CI/CD with Jenkins
- Monitoring Prometheus+Grafana
***
## Technology stack

- **Framework:** Flask (Python)
	I decide to use Flask instead of Django, because I don't have purpose to create something complex and big, i just need few pages and functions. In this view Flask looks more suitably.

- **Database**: MySQL
	 The most popular free relational database, i think it is classic decision. As minimum this site will contain articals with header and body, to identify them i will use id's.

- **Webserver**: gunicorn + Nginx
	 This combination offered in Flask documentation. 
	 Gunicorn is one of the most popular wsgi for python applications.
	 Nginx fast and simple decision to implement reverse proxy for gunicorn, Apache is overpowered for my case.

- **Source contol**: GitHub
	 I think explanation isn't required)

- **CI/CD**: Jenkins
	 Popular free tool, have a lot of modules and use cases.

- **Deploy**: Ansible 
	 Simple in use, python based and agentless, also very popular.

- **Build**: Docker
	 In my case i have not a lot of services for deploy and i can deploy them directly on host. But anyway i want to explore my knowledge of docker so why not?)

- **Host**: AWS
	 I  want to work with AWS, so i will test my project on AWS EC2 and RDS to make it ready to deploy on them.

***
## Instruction to deploy

1) Get a linux server (ubuntu22.04).
	I use ubuntu22.04 because it is popular and available to install on EC2.
2) Make sure you can connect to server from your machine via ssh.
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
	Aws playbook connect to remote MySQL using address and pass from env vars (hosts).
	Dev playbook connect to MySQL started in docker compose.  
7) Last stage of ansible playbook is response from aiblogger site. 
8) If you want to set up Jenkins for CI/CD, search for instruction below.

***
## App structure

- ### Project tree:
```
aiblogger
├── config.py
├── Dockerfile
├── .dockerignore
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
├── .gitignore
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

- #### config.py
	 file that contain configuration for flask app, and mysql connection

- #### Dockerfile
	File with instructions to build flask application for docker

- #### .dockerignore
	File that contains a list of files docker doesn't copy in app container.

- #### flaskr 
	 Directory that contains all files that Flask framework need to operate html requests.
	- \_\_init\_\_.py - file where we define our application (engine).
	- auth.py - code that defines functions of register and authentication.
	- blog.py - code that build main page with articles.
	- db.py - code in what we define functions to connect and initialize mysql.
	- static - directory that contain css properties
	- templates - directory that contain html templates for every page.
		base.html - define header that we use for every page

- #### .gitignore
	 File that contains list of file git doesn't push to aiblogger repo (pycache and python venv)

- #### ops
	Directory that contain configurations and playbooks to deploy.
	- ansible_playbooks - dir that store ansible playbooks
		host_deploy.sh bash script to deploy aiblogger without docker, but i didn't update it after adding new functionality( it won't work )
	- configs - dir that store nginx and gunicorn configs
		 You need gunicorn as a service only if you deploy aiblogger without docker.
		 If you deploy without docker, nginx will redirect requests to gunicorn socket.
	- docker-compose.yaml - file that describes what containers docker will start.
	- Jenkinsfile - file that contains instruction that Jenkins use to automatically deliver source code changes to remote server.

- #### README.md
	This file))

- #### requirements.txt
	File that contains a list of modules python need to start aiblogger.

- #### wsgi.py 
	File that contain instructions flask need to work with gunicorn.

***
## Flask

#### Flask is a simple web framework written in python.

- ##### Flask directory.
```
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

```

- #### Run application
	 To run application you should have installed flask and pymysql packages. I recommend to use python venv.
	 3 commands below will create py venv activate it and install all packages from requirements.txt
	 ```sh
	   python -m venv env
	   source env/bin/activate
	   pip install -r requirements.txt
    ```
	
	 After you install all packages you can start the application using pre-installed wsgi werkzeug.
	 ```sh
	flask --app flaskr --debug run
     ```
	 This command searches for \_\_init\_\_.py in flaskr folder and run it with parameter 'debug' that means your server will get changes from your code in real time.

	 But remember, to connect a database you should specify an environment variable CONFIG it can have 3 values Host, Dev or Prod depending on address and pass of your MySQL database, use Host if MySQL started on localhost. You can change config.py for your  needs.
	 ```sh
	export CONFIG='Host' 
    ``` 
	 This command will create an environment variable 'CONFIG' with value 'Host'.

- #### \_\_init\_\_.py define application 

	 Name of this file means that it will start first in folder.

	 Firstly of course we import Flask class. Also we import os package to use environment variables.
	 ```python
	from flask import Flask 
	import os
    ```

	 Next step is to create an instance of the Flask class, and give the name of our application.
	 ```python
	def create_app():
	 |   app = Flask(__name__)
	 |   ...
	 |   return app
    ```
	 As you can see, the argument \_\_name\_\_ will store the name of our application. 
	 Also you can see that our app is defined in the create_app() function, it is not necessarily but in future it will be very useful.

	 Next step is to define functions that will operate on requests the application receives.
	 ```python
		@app.route('/hello')
		def test():
		     return ' hello! '
    ```
	 In code above you see decorator route() that bind url( /hello ) to function test(). If you go to /hello you will see text from the return statement of test() function. 

***
To be continued...))
