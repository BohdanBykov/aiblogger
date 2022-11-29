# aiblogger
***
## Description

This must be a news website, with articles generated automatically by machine learning from real news. Maybe i will implement it in future, but now i use it as my pet project to try different DevOps tools and methods.

Below you will find blocks about deploy and configuration of this project:
- Technology stack
- Instruction to deploy
- App structure
- Flask
	 - Flask directory
	 - Run application
	 - Create the application (\_\_init\_\_.py)
	 - Set up database connection (db.py)
	 - Implement authentication(auth.py)
	 - Filling index page(blog.py)
	 - Contain configuration
- Nginx and gunicorn
- Docker compose
- Ansible playbooks
- CI/CD with Jenkins
- Monitoring Prometheus+Grafana
***
# Technology stack

- **Framework:** Flask (Python)
	I decided to use Flask instead of Django, because I don't have a purpose to create something complex and big, I just need a few pages and functions. In this view Flask looks more suitably.

- **Database**: MySQL
	 The most popular free relational database, I think it is a classic decision. At minimum this site will contain articles with header and body, to identify them i will use id's.

- **Webserver**: gunicorn + Nginx
	 This combination is offered in Flask documentation. 
	 Gunicorn is one of the most popular wsgi for python applications.
	 Nginx fast and simple decision to implement a reverse proxy for gunicorn, Apache is overpowered for my case.

- **Source contol**: GitHub
	 I think explanation isn't required)

- **CI/CD**: Jenkins
	 Popular free tool have a lot of modules and use cases.

- **Deploy**: Ansible 
	 Simple in use, python based and agentless, also very popular.

- **Build**: Docker
	 In my case I do not have a lot of services to deploy and I can deploy them directly on host. But anyway i want to explore my knowledge of docker so why not?)

- **Host**: AWS
	 I  want to work with AWS, so I will test my project on AWS EC2 and RDS to make it ready to deploy on them.

***
# Instruction to deploy

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
	Dev playbook connect to MySQL started in docker compose.  
7) Last stage of ansible playbook is a response from aiblogger site. 
8) If you want to set up Jenkins for CI/CD, search for instructions below.

***
# App structure

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

- ### config.py
	 file that contain configuration for flask app, and mysql connection

- ### Dockerfile
	File with instructions to build flask application for docker

- ### .dockerignore
	File that contains a list of files docker doesn't copy in app container.

- ### flaskr 
	 Directory that contains all files that Flask framework needs to operate html requests.
	- \_\_init\_\_.py - file where we define our application (engine).
	- auth.py - code that defines functions of register and authentication.
	- blog.py - code that build main page with articles.
	- db.py - code in what we define functions to connect and initialize mysql.
	- static - directory that contain css properties
	- templates - directory that contain html templates for every page.
		base.html - define header that we use for every page

- ### .gitignore
	 File that contains list of file git doesn't push to aiblogger repo (pycache and python venv)

- ### ops
	Directory that contains configurations and playbooks to deploy.
	- ansible_playbooks - dir that store ansible playbooks
		host_deploy.sh bash script to deploy aiblogger without docker, but i didn't update it after adding new functionality( it won't work )
	- configs - dir that store nginx and gunicorn configs
		 You need gunicorn as a service only if you deploy aiblogger without docker.
		 If you deploy without docker, nginx will redirect requests to gunicorn socket.
	- docker-compose.yaml - file that describes what containers docker will start.
	- Jenkinsfile - file that contains instructions that Jenkins use to automatically deliver source code changes to remote server.

- ### README.md
	This file))

- ### requirements.txt
	File that contains a list of modules python needs to start aiblogger.

- ### wsgi.py 
	File that contain instructions flask need to work with gunicorn.

***
# Flask

Flask is a simple web framework written in python.

- ### Flask directory.
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

***
- ### Run application
	 To run the application you should have installed flask and pymysql packages. I recommend using python venv.
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

	 To initialize database you can use init-db command
	 ```sh
	flask init-db
    ```

 
 ***
- ### Create the application (\_\_init\_\_.py)

	 Name of this file means that it will start first in folder.

	 Firstly of course we import Flask class. Also we import os package to use environment variables.
	 
	 ```python
	from flask import Flask 
	import os
	```

	 Next step is to create an instance of the Flask class, and give the name of our application.
	 
	```python
	def create_app():
	    app = Flask(__name__)
	    ...
	    return app
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
- ### Set up database connection (db.py)
	 This file contains functions that work with MySQL database, create and delete connections, and initialize tables that aiblogger need to store data.

	 #### At the start of the file we import packages.
	 ```python
	import pymysql
	import click
	from flask import g, current_app
    ```
	 - pymysql - is the package that can create database connections to execute mysql commands.
	 - click - is the package that we use to add init-db command to flask cli
	 - g - is flask’s namespace object that store data only for one session, work like stack but with only one item.
	 - current_app - is flask namespace object that store configuration of current app

	 #### get_db(), this function returns a g object with database connection in it.
	 ```python
    def get_db():
	    if 'db' not in g: 
	         g.db = pymysql.connect(
	              host=current_app.config['DBHOST'],
	              ...
	              cursorclass=pymysql.cursors.DictCursor
	              )
    return g.db
    ```
	 At the start we check if the g object already has 'db'(name that we give to the connection object).
	 If g doesn't store any connection we define connection using pymysql.connect() with values from config.py.
	 Next in the return statement as db we add this connection at the end of g.
	 In more detail about configuration handling in this project I will tell in last block.

	 #### close_db(), drop connection to database
	 ```python
	def close_db(e=None):
	     db = g.pop('db', None)
	     
	     if db is not None:
			db.close() 
    ```
	 Make db equal to g (must be None).
	 If g wasn't None, connection in db will be closed.

	 #### init_db(), execute list of mysql commands.
	 ```python
    def init_db():
    db = get_db()
    
    db.cursor().execute("DROP TABLE IF EXISTS post;")
    ...
    ```
	 In the first row we get a connection from get_db().
	 Using pymysql from connection we make cursor().
	 Cursor allows us to execute mysql commands as a user from configuration.
	 This commands will drop tables post and user if they already exist, create them after add columns to them.

	 #### sql tables and columns aiblogger use.
	 ```mysql
	 CREATE TABLE user (
	  id INTEGER PRIMARY KEY AUTOINCREMENT,
	  username TEXT UNIQUE NOT NULL,
	  password TEXT NOT NULL
	);

	CREATE TABLE post (
	  id INTEGER PRIMARY KEY AUTOINCREMENT,
	  author_id INTEGER NOT NULL,
	  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	  title TEXT NOT NULL,
	  body TEXT NOT NULL,
	  FOREIGN KEY (author_id) REFERENCES (user id)
	); 
    ```
	 This mysql script creates 2 tables user and post. 
	 - user table has columns 
		 - username
		 - password store hash generated from password written by user
		 - id that is unique, mysql server generate it automatically adding 1 to previous row
	 - post table has columns
		- id that is unique, mysql server generate it automatically adding 1 to previous row
		- author_id is equal to author's id in user table 
		- created store time when post was created, mysql server add it automatically
		- title 
		- body

	 #### init-db
	 Next functions we need to add the init-db command in flask cli command list.
	 
	 ```python
	@click.command('init-db')
	def init_db_command():
		init_db()
		click.echo('Initialized the database.')

	def init_app(app):
	    app.teardown_appcontext(close_db)
	    app.cli.add_command(init_db_command) 
    ```
	 
	 Decorator click defines 'init-db' command and connect it to function init_db_command()
	 This function calls the init_db() function we created above, and after click.echo shows a message in cli.
	 init_app() function add close_db() and init_db_command() to application context.

***
- ### Implement authentication(auth.py)



***
To be continued...))


