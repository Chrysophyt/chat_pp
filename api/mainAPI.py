from flask import Flask, request, jsonify, Response
from dbQuery import connectToMySQLdb, addMessage, getStatus, getMessage
app = Flask(__name__)

database = connectToMySQLdb('chat_pp')

def tryConnectDatabase():
    global database 
    database = connectToMySQLdb('chat_pp')

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