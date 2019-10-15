from flask import Flask, request, jsonify
from dbQuery import connectToMySQLdb, addMessage, getStatus, getMessage
app = Flask(__name__)

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
    if(database.is_connected()):
        messages = getMessage(database, 10)
        return jsonify(messages)
    return "ERROR_GET_MESSAGE"

@app.route('/api/get_status', methods=['GET'])
def get_status():
    if(database.is_connected()):
        return jsonify(status=getStatus(database))
    return "ERROR"

if __name__ == '__main__':
    app.run(debug=True)