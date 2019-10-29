from services.dbQuery import addAccount, verifyAccountInfo

def verifyLogin(username, password, database): #return bool true: data in db
    if(verifyAccountInfo(database, username)!= False): #data = ('username', 'pass') So, data[1]
        if(verifyAccountInfo(database, username)[1]==password):
            return True
    return False

def createAccount(username, password, database):
    status = addAccount(database, username, password)
    return status