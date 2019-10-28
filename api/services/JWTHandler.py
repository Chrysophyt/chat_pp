from flask import jsonify
import jwt
import datetime


def generateToken(secretkey):
    token = jwt.encode({'user' : 'Chrystian',
                         'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, secretkey)
    return token.decode('UTF-8')