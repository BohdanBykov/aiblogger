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

	 #### Import packages
	 ```python
	from flask import Flask 
	import os
	```
	 - flask - is main framework library
	 - os - library we will use in create_app() function to get environment varibles
	 
	 #### create_app(), function that defines app
	```python
	def create_app():
	    app = Flask(__name__)
	    ...
	    return app
	```
	 
	 As you can see, the argument \_\_name\_\_ will store the name of our application. 
	 Also you can see that our app is defined in the create_app() function, it is not necessarily but in future it will be very useful.

	 #### @app.route(), decorator that connect url to function
	```python
	@app.route('/hello')
	def test():
		return ' hello! '
	```
	 
	 In code above you see decorator route() that bind url( /hello ) to function test(). If you go to /hello you will see text from the return statement of test() function. 

***
- ### Set up database connection (db.py)
	 This file contains functions that work with MySQL database, create and delete connections, and initialize tables that aiblogger need to store data.

	 #### Import packages
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

	 #### init-db cli command
	 
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
	 In auth.py we create registration, authentication and logout pages. Also functions that checks is user logged in and decorator that block function if user didn't log in.

	 #### Import packages
	 ```python
	import functools
	from flask import (
	    Blueprint, flash, g, redirect, render_template, request, session, url_for
	)
	from werkzeug.security import check_password_hash, generate_password_hash
	from flaskr.db import get_db
	```
	 - functools - library that we will use to create login_required decorator
	 - flask (...) - couple of libraries that provide functionality to work with html templates and requests.
	 - werkzeug.security - packages we will use to generate and check hashed user passwords
	 - get_db - function from db.py that return connection to database

	 #### register(), function that save user to database
	 ```python 
	@bp.route('/register', methods=('GET', 'POST'))
	def register():
	    if request.method == 'POST':
	        username = request.form['username']
	        password = request.form['password']
	        db = get_db()
	        error = None
	```
	 Decorator @bp.route() will transmit GET and POST html requests from url '/register' to function.
	 First if triggered when user press button 'Register'(send information).
	 In the body of this if statement we define variables username/password with values from register form.
	 Next get connection and name it db, and define error var as a trigger to last if in register function.

	 ```python
			if not username:
				error = 'Username is required'
			if not password:
				error = 'Password is required'
    ```
	 Two if statements above create error message if username/password vars from previous if statement are emty (user didn't enter them)

	 ```python
			if error is None:
				try:
					db.cursor().execute(
					     "INSERT INTO user (username, password) VALUES(%s,%s)",
					     (username, generate_password_hash(password)),
					)
				     db.commit()
					except db.IntegrityError:
					     error = f"User {username} is already registered"
					else:
				          return redirect(url_for('auth.login'))
			flash(error) 
    ```
	 This if statement checks is var error defined previously is equal to None.
	 Next function try to execute SQL script that will add to user table values of username and password vars, but password will be hashed by function from werkzeug.security package.
	 If SQL execution was failed by IntegrityError, to error var will be added a message means username is already in the database.
	 Or if it was succesfull user will be automatically redirected to login page.
	 flash() funtion return value of error var if it wasn't None before if statement above.

	 ```python
		return render_template('auth/register.html') 
	```
	 register() function return html template from flaskr/templates/auth directory if user sends GET request.

	 #### login(), function search username/password written by user in db
	 ```python
	@bp.route('/login', methods=('GET','POST'))
	def login():
		if request.method == 'POST':
		     username = request.form['username']
			password = request.form['password']
		     db = get_db().cursor()
			error = None
		     select = db.execute(
			     'SELECT * FROM user WHERE username = %s', (username,)
			)
		     user = db.fetchone()
	```
	 Decorator @bp.route() will transmit GET and POST html requests from url '/login' to function.
	 First if triggered when user press button 'Log In'(send information).
	 In the body of this if statement we define variables username/password with values from login form.
	 Next get connection, name it db and add cursor() because we will use execute() separatly.
	 Define error var with default value None like in register() function.
	 Next step execute select SQL request that will return row with value from username var.
	 Finally define user var that will store data from previous request as a tuple.

	 ```python
		     if user is None:
				error = 'Incorrect username'
			elif not check_password_hash(user['password'], password):
			     error = 'Incorrect password'
	```
	 Two if statements above create error message if username/password vars from previous if statement are emty (user didn't enter them)
	 
	 ```python
			if error is None:
				session.clear()
				session['user_id'] = user['id']
				return redirect(url_for('index'))
			flash(error)

    ```
	 This if statement checks is var error defined previously is equal to None.
	 If it is default session will be cleared.(dict that stores data acrooss requests of current session)
	 After to 'user_id' key of session object we will add id of current user from database.
	 This allows browser to save cookie for registered users.
	 If login was succesfull user will be redirected to index(blog.py) page, else will be value of error var will be showed on the login page.

    ```python
		return render_template('auth/login.html') 
	```
	 login() function return html template(page) from flaskr/templates/auth directory if user sends GET request.

	 #### load_logged_in_user(), load data about user to g.user object
	 ```python
	@bp.before_app_request
	def load_logged_in_user():
		user_id = session.get('user_id')

		if user_id is None:
		     g.user = None
		else:
			db = get_db().cursor()
			select = db.execute(
				'SELECT * FROM user WHERE id = %s', (user_id,)
			)
			g.user = db.fetchone()
	```
	 Decorator @bp.before_app_requests() will activate function no matter what page user visited.
	 Firstly we define user_id var with value from session 'user_id' key.
	 First if statement checks is user have not user_id in session object.(means user is not logged in)
	 Else data from row with current user's id  will be added as a tuple to g.user object that stores information only for current session.

	 #### logout(), delete data about user for current session
	 ```python
	@bp.route('/logout')
	def logout():
	    session.clear()
	    return redirect(url_for('index'))

	```
	 Decorator @bp.route() will transmit html requests from url '/logout' to function.
	 session.clear() function removes user_id from the session object, so load_logged_in_user() won't load user info and add it to g.user.

	 #### login_requirred(), decorator function that checks is user logged in
	 ```python
	def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))
		return view(**kwargs)
	return wrapped_view 
	 ``` 
	 Define function, view means function with what decorator is used,  we will use it with blog.py functions.
	 Next using functools we register login_requirred() as a decorator.
	 wrapped_view() is function will be called by our decorator, (\*\*kwargs) means it can handle couple of views at the same time
	 If g.user doesn't know current user, login_reqquired() will redirect user to authentication page.
	 If g.user is defined decorator login_requirred() will return result of function on with it used for. 
	 
***
To be continued...))


