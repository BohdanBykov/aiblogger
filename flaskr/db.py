from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql

import click
from flask import current_app, g

# create_engine
engine = create_engine(current_app.config['DB_URL'], echo=True)

class User:
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, auto_increment=True)
    username = Column(String(10), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self. password = password

class Post:
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, auto_increment=True)
    author_id = Column(Integer, nullable=False)
    created = Column(nullable=False, )
