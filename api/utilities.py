import random
import string
import jwt
import re
import requests
from flask import jsonify
from .config import Config
from datetime import datetime, timedelta

def error(message,status):
    return jsonify({
        'success': False,
        'status': status,
        'message': message
    })

def success(message,data,status): 
    return jsonify({
        'success': True,
        'status': status,
        'message': message,
        'data': data
    })

def generateString(length):
    letters = string.ascii_letters
    result = ''.join(random.choice(letters) for i in range(length))
    return result

def create_jwt_token(data):
    expiration = datetime.utcnow() + timedelta(minutes=5)
    jwt_payload = {"data": data, "exp": expiration}
    jwt_token = jwt.encode(jwt_payload, Config.SECRET_KEY, algorithm="HS256")

    return jwt_token

def decode_jwt_token(token):
    decoded = jwt.decode(token, Config.SECRET_KEY, algorithms="HS256")
    return decoded

def senMail(message,email):
     x = requests.post("URL MAIL",json={
                "name": "RESHO121",
                "applicationId": "640f032982b64e15378a2cf7",
                "to": email,
                "subject": "Changement de mot de passe ",
                "type": "html",
                "message": message
                        })
     return x


def verifEmailAdress(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False