from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager, current_user
from flask_moment import Moment
import identity.web
import requests
# from flask_session import Session
from werkzeug.middleware.proxy_fix import ProxyFix

db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
login = LoginManager()
login.login_view = 'auth.login'


def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.static_folder = config_class.STATIC_FOLDER
    app.template_folder = config_class.TEMPLATE_FOLDER_MAIN
    #Session(app)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    app.jinja_env.globals.update(Auth=identity.web.Auth)  # Useful in template for B2C

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)

    # register blueprints

    from app.main import main_blueprint as main
    main.template_folder = Config.TEMPLATE_FOLDER_MAIN
    app.register_blueprint(main)

    from app.auth import auth_blueprint as auth
    auth.template_folder = Config.TEMPLATE_FOLDER_AUTH
    app.register_blueprint(auth)

    from app.errors import error_blueprint as errors
    errors.template_folder = Config.TEMPLATE_FOLDER_ERRORS
    app.register_blueprint(errors)

    from app.instructor import instructor_blueprint as instructor
    instructor.template_folder = Config.TEMPLATE_FOLDER_INSTRUCTOR
    app.register_blueprint(instructor)

    from app.student import student_blueprint as student
    student.template_folder = Config.TEMPLATE_FOLDER_STUDENT
    app.register_blueprint(student)

    return app
