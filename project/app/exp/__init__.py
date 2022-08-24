from flask import Blueprint

exp = Blueprint('exp', __name__, template_folder='templates')

from . import routes

