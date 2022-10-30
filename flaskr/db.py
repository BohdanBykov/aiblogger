import pymysql

import click
from flask import current_app, g

import sys
sys.path.append("..")
from instance.config import MYSQL_CONFIG 

def get_db():
    if 'db' not in g:
        cfg = MYSQL_CONFIG
        g.db = pymysql.connect(
            host=cfg.host,
            user=cfg.user,
            password=cfg.password,
            database=cfg.database,
            cursorclass=cfg.cursorclass
            )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

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


@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    #add new command to flask (use in terminal)
    app.cli.add_command(init_db_command)




