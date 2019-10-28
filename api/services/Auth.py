from services.dbQuery import addAccount

def verifyLogin(username, password): #return bool true: data in db
    print('verify')
def checkUsername(username): #return bool true: available
    print('checkUsername')

def createAccount(username, password, database):
    status = addAccount(database, username, password)
    return status