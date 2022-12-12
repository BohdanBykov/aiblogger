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

# when mysql and flask in docker 
class Test(Config):
        DBHOST = '172.18.0.2'
        DBPASS = 'password'
        SECRET_KEY = 'dev'

        DEBUG = True
        TESTING = True

# when mysql server remote
class Prod(Config):
        DBHOST = os.environ.get('DBHOST')
        DBPASS = os.environ.get('DBPASS')
        SECRET_KEY = os.environ.get('SECRET_KEY')
