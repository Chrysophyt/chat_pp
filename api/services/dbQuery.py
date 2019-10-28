import mysql.connector
#table schema
#chat_data(id int AUTO_INCREMENT, username text, message text, primary key(id));
#account_data(username VARCHAR(50), password VARCHAR(50), primary key(username));

add_message = ("INSERT INTO chat_data "
               "(username, message) "
               "VALUES (%s, %s)")

get_message = ("SELECT * FROM chat_data "
               "ORDER BY ID DESC "
               "LIMIT %s")

get_status =("SELECT MAX(ID) FROM chat_data")

create_account = ("INSERT INTO account_data "
               "(username, password) "
               "VALUES (%s, %s)")

def connectToMySQLdb(database_name):
    database = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd="",
        database= database_name #pastikan sudah ada db nama ini
    )
    return(database)

def addMessage(database, data):
    message_data = (data['username'], data['message'])
    cursor = database.cursor()
    cursor.execute(add_message, message_data)

def addAccount(database, username, password):
    account_data = (username, password)
    cursor = database.cursor()
    try:
        cursor.execute(create_account, account_data)
        database.commit()
        return "Success"
    except mysql.connector.errors.IntegrityError:
        return "Sorry, the username already been taken"

def getStatus(database):
    cursor = database.cursor()
    cursor.execute(get_status)
    data = cursor.fetchall()
    return(data[0][0])

def getMessage(database, amount):
    cursor = database.cursor()
    parameter = (int(amount),)
    cursor.execute(get_message, parameter)
    data = cursor.fetchall()
    return(data)
    