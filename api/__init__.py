
from flask import Flask
from flask_cors import CORS
from flask_compress import Compress
from flask_marshmallow import Marshmallow
from .config import Config
import mongoengine as orm_db
from flask_session import Session
import certifi
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)

api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

sess = Session()
sess.init_app(app)

ma = Marshmallow(app)

db = orm_db
# db.connect(host=Config.MONGO_URI, alias="default", tlsCAFile=certifi.where())
db.connect(host=Config.MONGO_URI, alias="default")
Compress(app)

from .scraping import scraping as scraping_blueprint


app.register_blueprint(scraping_blueprint, url_prefix="/scraping")
# app.register_blueprint(admin_blueprint, url_prefix="/admin")
# app.register_blueprint(auth_blueprint, url_prefix="/auth")

CORS(app, resources={r"/*": {"origins": "*"}}, headers='Content-Type')