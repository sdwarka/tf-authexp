from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#---------------------------------------------------------
# init SQLAlchemy so we can use it later in our models
#---------------------------------------------------------
db = SQLAlchemy()

#---------------------------------------------------------
# init a LoginManager so we can use it later
#---------------------------------------------------------
login_manager = LoginManager()

##########################################################
# function to create, configure and return the Flask app
##########################################################
def create_app():

    app = Flask(__name__)

    # TODO: use the config module here
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # blueprint for auth routes in our app
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for expense entry
    from .exp import exp as exp_blueprint
    app.register_blueprint(exp_blueprint)

    return app

