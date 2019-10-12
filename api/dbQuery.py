import mysql.connector
#table_schema query:
# 
#create table 
#chat_data(id int AUTO_INCREMENT, username text, message text, primary key(id));

add_message = ("INSERT INTO chat_data "
               "(username, message) "
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
    message_data = ('', data['message'])
    cursor = database.cursor()
    cursor.execute(add_message, message_data)
    
