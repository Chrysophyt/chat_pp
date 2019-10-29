from flask import Flask, request, jsonify, Response
import jwt
import datetime
from functools import wraps

from services.dbQuery import connectToMySQLdb, addMessage, getStatus, getMessage
#from services.JWTHandler import generateToken
from services.Auth import createAccount, verifyLogin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
database = connectToMySQLdb('chat_pp')

def tryConnectDatabase():
    global database 
    database = connectToMySQLdb('chat_pp')

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('access-token')
        if(token==None):
            return jsonify(error='No Session Found.'), 401 #Unauthorized
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            #print(data)
            return jsonify(error='Session is invalid.'), 403 #Forbidden

        return f(*args, **kwargs)
    return decorated

@app.route('/api/validate', methods=['GET'])
@auth_required
def validate():
    return jsonify(status='Ok'), 200

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    if(verifyLogin(data['username'], data['password'], database)):
        token = jwt.encode({'username' : data['username'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        res = Response(status=200)
        res.set_cookie('access-token', token.decode('UTF-8'))
        return res
    return jsonify(error="Sorry, Wrong Login data."), 406 #Not Acceptable

@app.route('/api/create_account', methods=['POST'])
def create_account():    
    data = request.get_json()
    print(data)
    result = ""
    if(database.is_connected()):
        result = createAccount(data['username'], data['password'], database)
    else:
        tryConnectDatabase()
        return jsonify(error="Database is down. :("), 503 #Service Unavailable

    if(result!="Success"):
        return jsonify(status=result), 406 #Not Acceptable

    return jsonify(status=result)

@app.route('/api/send_message', methods=['POST'])
@auth_required
def send_message():
    data = request.get_json()
    if(database.is_connected()):
        addMessage(database, data)
    database.commit()

    return jsonify(status='Ok'), 200

@app.route('/api/get_message', methods=['GET'])
def get_message():
    data = request.args.get('amount')
    print("message sent :"+str(data))
    if(database.is_connected()):
        messages = getMessage(database, data)
        return jsonify(messages)

    tryConnectDatabase()
    return jsonify(error="ERROR_GET_MESSAGE"), 503 #Service Unavailable

@app.route('/api/get_status', methods=['GET'])
def get_status():
    if(database.is_connected()):
        return jsonify(status=getStatus(database))

    tryConnectDatabase()
    return jsonify(error="ERROR_GET_STATUS"), 503 #Service Unavailable

if __name__ == '__main__':
    app.run(debug=True)