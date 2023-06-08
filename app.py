
from api import app
import logging
import os
from logging.handlers import TimedRotatingFileHandler

filepath = 'logs'

os.makedirs(filepath, exist_ok=True)
LOG_FORMAT = ("%(asctime)s [%(levelname)s]: %(message)s in %(pathname)s:%(lineno)d")
handler = TimedRotatingFileHandler(filepath+'/resho_121.log', when="midnight", interval=1, encoding='utf8')

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt='%Y-%m-%dT%H:%M:%S', handlers=[handler])

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, threaded=True)
