from flask import Flask, request, jsonify
from dbQuery import connectToMySQLdb, addMessage
app = Flask(__name__)

#nama database mysql chat_pp bebas sebenarnya
database = connectToMySQLdb('chat_pp') 

@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    if(database.is_connected()):
        addMessage(database, data)
    database.commit()

    return jsonify(status='success')

@app.route('/api/get_message', methods=['GET'])
def index():
    print("GET")#belum selesai
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)