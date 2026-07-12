from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os


load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__) #, instance_relative_config=True)
 
    app.config['SECRET_KEY'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True
    }

    db.init_app(app)
    migrate.init_app(app, db)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    #os.makedirs(app.instance_path, exist_ok=True)

    # a simple page that says hello
    @app.route('/hello/')
    def hello():
        return 'Hello, World!'
    

    # from . import db
    from . import auth
    from . import notes

    # db.init_app(app)
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(notes.bp)
    app.add_url_rule('/', endpoint='index')

    return app