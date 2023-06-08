import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    MONGO_URI = os.environ.get('MONGO_URI')
    JWT_SECRET_KEY  = os.environ.get('JWT_SECRET_KEY')
    UPLOAD_FOLDER = os.path.join(basedir, 'static/docs')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAX_CONTENT_LENGTH = 4 * 1024 * 1024
    EXPORT_PATH = os.environ.get('EXPORT_PATH')