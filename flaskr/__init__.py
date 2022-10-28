import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')


    # test page
    @app.route('/test')
    def hello():
        return 'test page'

    from . import auth
    app.register_blueprint(auth.bp)

    from  . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    from . import db
    with app.app_context():
        db.init_db()

    return app
