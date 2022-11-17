# lib to connect to mysql
import pymysql
# lib to add init-db command to flask server
import click
# g is object that store db connection like g.connection
from flask import g, current_app


# return connection to db 
def get_db():
    # if g doesn't store any connection yet
    if 'db' not in g:
        g.db = pymysql.connect(
            host=current_app.config['DBHOST'],
            user=current_app.config['DBUSER'],
            password=current_app.config['DBPASS'],
            database=current_app.config['DBNAME'],
            cursorclass=pymysql.cursors.DictCursor
            )
    return g.db

# remove connection from g
def close_db(e=None):
    db = g.pop('db', None)

    # if connection store comething
    if db is not None:
        db.close()

# create tables
def init_db():
    db = get_db()

    # drop tables
    db.cursor().execute("DROP TABLE IF EXISTS post;")
    db.cursor().execute("DROP TABLE IF EXISTS user;")

    # create table user
    db.cursor().execute( ' CREATE TABLE user( '
                ' id INTEGER PRIMARY KEY AUTO_INCREMENT,'
                ' username varchar(10) UNIQUE NOT NULL,'
                ' password varchar(256) NOT NULL'
                ');' )

    # create table post
    db.cursor().execute( ' CREATE TABLE post( '
                'id INTEGER PRIMARY KEY AUTO_INCREMENT,'
                'author_id INTEGER NOT NULL,'
                'created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,'
                'title varchar(20) NOT NULL,'
                'body varchar(500) NOT NULL,'
                'FOREIGN KEY (author_id) REFERENCES user (id)'
                ');' )

# bind init_db function to 'init-db' option 
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

# add option 'init-db' to flask app
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)




