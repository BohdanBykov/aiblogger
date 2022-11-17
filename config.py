# static settings
class Config(object):
	DEBUG = False
	TESTING = False
	SECRET_KEY = 'Testedsdaggefvgvwrbvbvda'

	DBUSER = 'site'
	DBNAME = 'site_db'
	DBPASS = 'password'

# when flask and mysql on one host
class Host(Config):
	DBHOST = 'localhost'

# when you use docker compose 
class Docker(Config):
	DBHOST = '172.18.0.2'

# when flask on host but mysql in container
class DbInDocker(Config):
	DBHOST = '172.17.0.1'