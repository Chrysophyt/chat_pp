import mysql.connector
#table schema 
#create table 
#chat_data(id int AUTO_INCREMENT, username text, message text, primary key(id));
add_message = ("INSERT INTO chat_data "
               "(username, message) "
               "VALUES (%s, %s)")

get_message = ("SELECT * FROM chat_data "
               "ORDER BY ID DESC "
               "LIMIT %s")

get_status =("SELECT MAX(ID) FROM chat_data")


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
    