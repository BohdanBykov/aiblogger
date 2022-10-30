import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')


    # test page
    @app.route('/hello')
    def test():
        return ' hello! '


    from . import auth
    app.register_blueprint(auth.bp)

    from  . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    from . import db
    db.init_app(app)

    # with app.app_context():
    #     db.get_db()


    return app
