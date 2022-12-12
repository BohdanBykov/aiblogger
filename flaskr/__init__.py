import os
from flask import Flask


def create_app():
    # create and configure the app
    app = Flask(__name__)
    # get config from env var CONFIG, if not default value Host
    environ_config = os.environ.get('CONFIG', 'Host')
    app.config.from_object('config.' + environ_config)

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
