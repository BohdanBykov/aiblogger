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
	 - Configuration management(config.py)
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

	 #### define authentication blueprint
	 ```python
	bp = Blueprint('auth', __name__, url_prefix='/auth') 
	```
	 Blueprint is the html file/template, default path is flaskr/templates.
	 We create blueprint for authentication pages, path to them will be flaskr/templates/auth.
	 \_\_name\_\_ store name of our app, which will use this template.
	 url_prefix means that this blueprint will be used with urls after '/auth' (/auth/login /auth/register)
	 
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
	 First if triggered when the user presses the button 'Log In'(send information).
	 In the body of this if statement we define variables username/password with values from login form.
	 Next get connection, name it db and add cursor() because we will use execute() separatly.
	 Define error var with default value None like in register() function.
	 Next step execute select SQL request that will return row with value from username var.
	 Finally define a user var that will store data from previous requests as a tuple.

	 ```python
		     if user is None:
				error = 'Incorrect username'
			elif not check_password_hash(user['password'], password):
			     error = 'Incorrect password'
	```
	 Two if statements above create error message if username/password vars from previous if statement are empty (user didn't enter them)
	 
	 ```python
			if error is None:
				session.clear()
				session['user_id'] = user['id']
				return redirect(url_for('index'))
			flash(error)

    ```
	 This if statement checks if var error defined previously is equal to None.
	 If it is default session will be cleared.(dict that stores data across requests of current session)
	 After the 'user_id' key of the session object we will add the id of the current user from the database.
	 This allows browsers to save cookies for registered users.
	 If login was successful the user will be redirected to the index(blog.py) page, else the value of error var will be shown on the login page.

    ```python
		return render_template('auth/login.html') 
	```
	 login() function returns html template(page) from flaskr/templates/auth directory if the user sends a GET request.

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
	 Decorator @bp.before_app_requests() will activate the function no matter what page the user visited.
	 Firstly we define user_id var with the value from session 'user_id' key.
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
	 If g.user doesn't know the current user, login_reqquired() will redirect the user to the authentication page.
	 If g.user is defined, the decorator login_requirred() will return the result of the function on which it was used for. 
	 
***
- ### Main page with posts(blog.py)
	 In blog.py we define functions that fill index pages on url '/', and functions that allow users to create, update and delete posts on the main page.

	 #### Import packages
	 ```python
	 from flask import (
	    Blueprint, flash, g, redirect, render_template, request, url_for
	)
	from werkzeug.exceptions import abort

	from flaskr.auth import login_required
	from flaskr.db import get_db
	```
	 - flask (...) - couple of libraries that provide functionality to work with html templates and requests.
	 - abort - function that return to user error page (404 at example)
	 - @login_required - decorator defined in auth.by, that can block function to unregistered user.
	 - get_db() - function that returns connection to database.

	 #### define blog blueprint
	 ```python
	bp = Blueprint('blog', __name__) 
	```
	 Blueprint is the html file/template, default path is flaskr/templates.
	 We register blueprint for blog pages, path to them will be flaskr/templates/blog.
	 \_\_name\_\_ store name of our app, which will use this template.
	 url_prefix for this blueprint is default '/', we don't need to specify it.

	 #### get_post(), search for post in database by id
	 ```python
	def get_post(id, check_author=True):
		db = get_db().cursor()
		select = db.execute(
			'SELECT p.id, title, body, created, author_id, username'
			' FROM post p JOIN user u ON p.author_id = u.id'
			' WHERE p.id = %s', (id,)
		)
		post = db.fetchone()

		if post is None:
			abort(404, f"Post id {id} doesn't exist")
	
		if check_author and post['author_id'] != g.user['id']:
			abort(403)

		return post 
	```
	 Define function with post id and check_author parameter which means this function can get_post even without defined author_id(it isn't used here)
	 Next, get a connection to the database with a cursor, because we will use the execute() function separately.
	 Next step: execute select SQL request that will return values from post table and synchronize author_id column with id column from user table.
	 Define a post variable that will store post data from previous SQL execution as a tuple.
	 If the post variable is None (post with this post_id didn't finded in database) status 404 page will be returned to the user.
	 If the function didn't check the author, the status 403 page will be returned to the user.
	 Finally get_post() returns the data of the post with the given id as a single tuple.

	 #### index(), fill '/' page with latest posts
	 ```python
	@bp.route('/')
	def index():
		db = get_db().cursor()
		select = db.execute(
			'SELECT p.id, title, body, created, author_id, username'
			' FROM post p JOIN user u ON p.author_id = u.id'
			' ORDER BY created DESC'
		)
		posts = db.fetchall()
		return render_template('blog/index.html', posts=posts)
	```
	 Decorator @bp.route() will transmit GET html requests from url '/' to function.
	 Next get connection, name it db and add cursor() because we will use execute() separately.
	 Next step is to execute select SQL request that will return values from the post table and synchronize the author_id column with the id column from the user table.
	 After defining posts var that will store data from previous requests, where each row is a tuple.
	 Finally return blog template with posts variable passed in it.

	 ```python
	@bp.route('/create', methods=('GET', 'POST'))
	@login_required
	def create():
		if request.method == 'POST':
			title = request.form['title']
			body = request.form['body']
			error = None
	```
	 Decorator @bp.route() will transmit GET and POST html requests from url '/create' to function.
	 User is automatically redirected to /create when push the button "Create" in the top right corner.
	 Decorator @login_required activate create() only if current user is logged in.
	 In the body of this if statement we define variables title/body with values from the create form.
	 Define variable error with default value None.

	 ```python
			if not title:
				error = 'Title is required'
			if error is not None:
				flash(error)
			else:
				db = get_db()
				db.cursor().execute(
				     'INSERT INTO post (title, body, author_id)'
					' VALUES (%s,%s,%s)', (title, body, g.user['id'])
				)
			     db.commit()
				return redirect(url_for('blog.index'))
     ```
	 The Second if statement checks if the user didn't print any title, if yes the value of error var will be changed to message.
	 The Third if statement triggered if value error is a message, this message will be displayed by function flash().
	 Else value of error is None, get connection, name it db.
	 Next execute insert SQL command with values from title and body, also add author_id from g.user.
	 After the db.commit() function which saves these changes to the database, users will be redirected to index page '/'.

	 ```python
	    return render_template('blog/create.html') 
	```
	 create() function return to user create.html template by default.

	 #### update(), function that allows users to change posts.
	 ```python
	@bp.route('/<int:id>/update', methods=('GET', 'POST'))
	@login_required
	def update(id):
		post = get_post(id)

		if request.method == 'POST':
			title = request.form['title']
			body = request.form['body']
			error = None
	```
	 Decorator @bp.route() will transmit GET and POST html requests from url '/(post id)/update' to function.
	 User is automatically redirected to /update when push the button "Update" in the top right corner.
	 Decorator @login_required activates update() only if current user is logged in.
	 Define variable post value from get_post() function, that returns post data from database by post id.
	 In the body of this if statement we define variables title/body with values from the update form.
	 Define variable error with default value None.

	 ```python
			if not title:
				error = 'Title is required'

			if error is not None:
				flash(error)
			else:
				db = get_db()
				db.cursor().execute(
					'UPDATE post SET title = %s, body = %s WHERE id = %s',
					(title, body, id)
				)
				db.commit()
				return redirect(url_for('blog.index'))
	```
	 The Second if the statement checks if the user didn't print any title, if yes the value of error var will be changed to message.
	 The Third if statement triggered if value error is a message, this message will be displayed by function flash().
	 Else value of error is None, get connection, name it db.
	 Next step is execute an update SQL command which will update row with current post id by values from title and body variables.
	 After the db.commit() function which saves these changes to the database, user will be redirected to index page '/'.

	 ```python
		return render_template('blog/update.html', post=post) 
	```
	 update() function returns a user update.html template with data of the current post by default.

	 #### delete(), function that allows user to delete post
	 ```python
	@bp.route('/<int:id>/delete', methods=('POST',))
	@login_required
	def delete(id):
		get_post(id)
		db = get_db()
		db.execute('DELETE FROM post WHERE id = %s', (id,))
		db.commit()

		return redirect(url_for('blog.index'))
	```
	 Decorator @bp.route() will transmit POST html requests from url '/(post id)/delete' to function.
	 User is automatically redirected to /delete when push the button "Create" in the top right corner.
	 Decorator @login_required activates delete() only if current user is logged in.
	 Define variable post value from get_post() function, that returns post data from database by post id.
	 Get connection to the database.
	 After we execute the DELETE SQL command that will delete row with current post id from the database.
	 Finally the db.commit() function will save changes to the database, and the user will be redirected to index page '/'.

***
- ### Configuration management(config.py)

	 #### Which parameters aiblogger app should store.
	 - Flask
		 - DEBUG - if True your wsgi will be automatically update site with changes in code (useful for develop)
			 In production DEBUG should be false
		- SECRET_KEY - key which will be used by the flask application to securely signing session cookie.
	 - MySQL
		- DBHOST - address of mysql server
		- DBNAME - name of the database to which pymysql will connects 
			(mysql server has separated databases with tables)
		- DBUSER - username pymysql(db.py) will use to connect to the database
		- DBPASS - password pymysql(db.py) will use to connect to the database

	 #### config.py
	 This file is in the root directory 'aiblogger/config.py', so you don't need to go too deep to change it.
	 ```python
	import os
	# static settings
	class Config(object):
	   DEBUG = False
        TESTING = False
        
        DBUSER = 'site'
        DBNAME = 'site_db'

	# when flask and mysql on one host
	class Host(Config):
        DBHOST = 'localhost'
        DBPASS = 'password'
        SECRET_KEY = 'dev'

	# when mysql and flask in docker compose
	class Dev(Config):
        DBHOST = '172.18.0.2'
        DBNAME = 'password'
        SECRET_KEY = 'dev'
	# when mysql server is remote
	class Prod(Config):
        DBHOST = os.environ['DBHOST']
        DBPASS = os.environ['DBPASS']
        SECRET_KEY = os.environ['SECRET_KEY']
	``` 
	 You can see parent class 'Config' and 3 child classes 'Host' 'Dev' and 'Prod' that inherit from it.
	 In parent class 'Config' you see settings which will be used by each child class. 
	 DEBUG and TESTING parameters you should set True in config you want to use for development.
	 'Host' and 'Dev' I use to deploy on virtual machines so I don't need to hide data for them.
	 'Prod' config I use to deploy on AWS EC2 and RDS, so I can't push parameters in the public github repo.
	 To securely pass parameters I store them in environment variables DBHOST DBPASS and SECRET_KEY.
	 While deploying Ansible, set them using values defined locally in the inventory file. 
	 
	 #### How app get configuration
	 ```python
	# __init__.py
	def create_app():
		app = Flask(__name__)
		environ_config = os.environ['CONFIG']
		app.config.from_object('config.' + environ_config) 
	```
	 environ_config is a variable which gets value from the environment variable CONFIG using os package.
	 app.config.from_object('pathtofile.object') is construction by what flask app load configuration.
	 For flask app 'aiblogger/' is a root directory, so 'aiblogger/config.py' will be just 'config.py'.
	 Path to the config file is static, but the name of the object(class) can be Host,Dev or Prod. To specify one of them I use the environment variable CONFIG, value of what will be added after 'config.' as a variable environ_config.

	 To set env var CONFIG in linux use code below:
	 ```sh
	export CONFIG='Host' 
	``` 
	 
	 #### How ansible set env vars while deploy
	 ```yml
	#ops/ansible_playbooks/docker_deploy_aws.yaml 
        - name: docker compose up
          community.docker.docker_compose:
            project_src: /home/ubuntu/aiblogger/ops/
          
          # aws:vars in hosts
          environment:
            CONFIG: "{{ config }}"
            DBHOST: "{{ mysql_host }}"
            DBPASS: "{{ mysql_pass }}"
            SECRET_KEY: "{{ secret_key }}"
          register: output
	```
	 This is ansible playbook stage where we start docker compose.
	 In the last block we set environment variables that will be defined in docker containers.
	 Values of these variables ansible take from inventory.
	 By default ansible inventory is in file /etc/ansible/hosts.
	 ```sh
	[vm]
	111.111.111.111

	[vm:vars]
	...
	config = 'Prod'
	mysql_host = '123.123.123.123'
	mysql_pass = 'password'
	secret_key = 'example_secret_key'
	```
	 It is an ordinary ansible inventory file in brackets \[vm\] you set name of the group, below them ip or domain name of target machines.
	 In the next brackets \[vm:vars\] you specify parameters, there I create variables which I used in the playbook above.
	 
***
# Nginx and gunicorn

Nginx is a fast multifunctional web server written in C language. 
In this project it is used as a reverse proxy server, it will catch and redirect all http requests to gunicorn wsgi.

WSGI is a web server gateway interface designed for web servers to forward requests to python web applications.
Gunicorn is a WSGI server, it will transfer requests between Nginx and flask application. 

- ### Configure app to work with wsgi and proxy server.
	 ```python
	# wsgi.py
	from flaskr.__init__ import create_app
	from werkzeug.middleware.proxy_fix import ProxyFix
	import pymysql

	app = ProxyFix(create_app(), x_for=1, x_host=1, x_proto=1)
	```
	 In the first row import create_app() function that stores our application.
	 Next import ProxyFix package, using it we limit the count of proxy servers our app will trust.
	 Finally create an app object using ProxyFix, to this object we pass our original app object, and parameters.
	 
	 Parameters you see are given by Nginx, and you will see it again in nginx docker config file.
	 (x_for) X-Forwarded-For            sets remote address
	 (x_host) X-Forwarder-Host        sets http_host, server_name and server_port
	 (x_proto) X-Forwarded-Proto    sets wsgi.url_scheme.

- ### Configure gunicorn

	 #### Start gunicorn on host
	 gunicorn must be installed by pip as  a python package.
	 To start gunicorn as a server to flask app use the command below.
	```sh
	gunicorn --workers 3 wsgi:app
	```
	 This command will start the object "app" from the wsgi.py file.

	 #### Start gunicorn in docker container(Test, Prod)
	 ```yml
	flask:
	build: 
		context: ../
		dockerfile: Dockerfile
	environment:
		- CONFIG=$CONFIG
		...
	command: sh -c "cd /aiblogger && gunicorn --bind 0.0.0.0:8000 wsgi:app"
	... 
	```
	 Details about how I use Docker will be in another block, but this code describes configuration which docker uses to build containers for our app.
	 Last row is a command block, it will execute sh(shell) -c(command) right after container build. 
	 This command is similar to previous but with --bind parameter instead of --workers.
	 --bind 0.0.0.0:8000 means that the gunicorn server will be started on 0.0.0.0 address.
	 0.0.0.0 address is special, it means that anybody can connect to the current machine.
	 Practically nginx will connect to it by address 172.18.0.3 (address of container in docker compose).

	 #### Start gunicorn as a unix service(Host)
	 ```sh
	#ops/configs/gunicorn.service
	[Unit]
	Description=gunicorn daemon
	Requires=gunicorn.socket
	After=network.target

	[Service]
	User=ubuntu
	Group=ubuntu
	WorkingDirectory=/srv/aiblogger
	ExecStart=/srv/aiblogger/env/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          wsgi:app

	[Install]
	WantedBy=multi-user.target
	```
	 This is a service unit that describes how to manage gunicorn application.
	 In \[Unit] block you can see that gunicorn service requires gunicorn.socket, it will trigger service to start.
	 Directive 'After=' means that network management software will be started before gunicorn service.
	 In \[Service] block we execute a command that will start gunicorn binded to gunicorn.socket.
	 While deploy process gunicorn.socket will copied to /etc/systemd/system directory

	 ```sh
	# ops/configs/gunicorn.socket
	[Unit]
	Description=gunicorn socket

	[Socket]
	ListenStream=/run/gunicorn.sock

	[Install]
	WantedBy=sockets.target
	```
	 This is a socket unit file that describes gunicorn socket work.
	 It will create gunicorn.sock to which nginx will redirect requests.

	 #### Nginx configuration(Host)
	 ```sh
	# ops/configs/host_nginx.conf
	events {
		worker_connections 1024;
	}
	http {
		server{
			listen      80;
			server_name localhost;
			
			#default
			access_log /var/log/nginx/access.log;
			error_log  /var/log/nginx/error.log;
			
			location / {
				include proxy_params;
				proxy_pass http://unix:/run/gunicorn.sock;
			}
		}
	}
	```
	 There you can see the nginx config file.
	 In "events" block  we choose the count of connections each worker(nginx process) will operate.
	 In "server" block we choose from what address nginx server will receive requests, by default localhost:80.

	 #### Nginx configuration(Test, Prod)
	 ```sh
	# ops/configs/docker_nginx.conf
	events {
		worker_connections 1024;
	}

	http {
		server{
			listen      80;
			server_name localhost;

			#default
			access_log /var/log/nginx/access.log;
			error_log  /var/log/nginx/error.log;

			location / {
				proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
				proxy_set_header X-Forwarded-Proto $scheme;
				proxy_set_header Host $http_host;

				proxy_pass http://172.18.0.3:8000;
			}
		}
	}
	```
	 Difference between host and docker nginx configs is in "location" block.
	 For Docker deploy we specify the ip address of the docker container where gunicorn started serviceless.
	 Also there are proxy parameters I specify manually.
	 
***
To be continued...))






