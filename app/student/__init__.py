from flask import Blueprint

student_blueprint = Blueprint('student', __name__)

from app.student import student_routes

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_login import LoginManager
# TODO: (milestone 3) import LoginManager and Moment extensions here



db = SQLAlchemy()

migrate = Migrate()
moment = Moment()

login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
# TODO: (milestone 3) create LoginManager object and configure the login view as 'auth.login', i.e, `login` route in `auth` Blueprint. 
# TODO: (milestone 3) create Moment object


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.static_folder = config_class.STATIC_FOLDER
    app.template_folder = config_class.TEMPLATE_FOLDER_MAIN

    db.init_app(app)
    migrate.init_app(app,db)
    moment.init_app(app)
    login.init_app(app)
    # TODO: (milestone 3) Configure the app object for login using `init_app` function. 
    # TODO: (milestone 3) Configure the app object for moment using `init_app` function. 

    # blueprint registration
    from app.main import main_blueprint as main
    main.template_folder = Config.TEMPLATE_FOLDER_MAIN
    app.register_blueprint(main)

    from app.auth import auth_blueprint as auth
    auth.template_folder = Config.TEMPLATE_FOLDER_AUTH
    app.register_blueprint(auth)

    from app.errors import error_blueprint as errors
    errors.template_folder = Config.TEMPLATE_FOLDER_ERRORS
    app.register_blueprint(errors)

    return app