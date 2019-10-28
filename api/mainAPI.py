from flask import Flask, request, jsonify, Response
from services.dbQuery import connectToMySQLdb, addMessage, getStatus, getMessage
from services.JWTHandler import generateToken
from services.Auth import createAccount

app = Flask(__name__)

database = connectToMySQLdb('chat_pp')

def tryConnectDatabase():
    global database 
    database = connectToMySQLdb('chat_pp')


@app.route('/api/login', methods=['POST'])
def login():
    
    return jsonify({'token' : generateToken('SECRET_KEY')})

@app.route('/api/create_account', methods=['POST'])
def create_account():    
    data = request.get_json()
    print(data)
    if(database.is_connected()):
        createAccount(data['username'], data['password'], database)
    else:
        tryConnectDatabase()
        
    return jsonify(status='success')

@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    if(database.is_connected()):
        addMessage(database, data)
    database.commit()

    return jsonify(status='success')

@app.route('/api/get_message', methods=['GET'])
def get_message():
    data = request.args.get('amount')
    print("message sent :"+str(data))
    if(database.is_connected()):
        messages = getMessage(database, data)
        return jsonify(messages)

    tryConnectDatabase()    
    return Response("ERROR_GET_MESSAGE", status=503)

@app.route('/api/get_status', methods=['GET'])
def get_status():
    if(database.is_connected()):
        return jsonify(status=getStatus(database))

    tryConnectDatabase()
    return Response("ERROR_GET_STATUS", status=503)

if __name__ == '__main__':
    app.run(debug=True)