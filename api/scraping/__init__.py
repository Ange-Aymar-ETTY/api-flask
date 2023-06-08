from flask import Blueprint
from flask_restful import Api

scraping = Blueprint('scraping', __name__)
api = Api(scraping)
 
from . import routes