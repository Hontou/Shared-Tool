from User import *
from Tool import *

def createNewUser():
    userForename = input('> Forename: ')
    userSurname = input('> Surname: ')
    userAddress = input('> Address: ')
    userEmail = input('> Email: ')
    userPassword = input('> Password: ')
    user = User.createUser(userForename, userSurname, userAddress,userEmail,userPassword)
    print('New user with id: ' + str(user) + ' created.')

def AllUsers():
    filePath = User.Path('userdata')
    stored = []
    for file in os.listdir(filePath):
        if file.endswith(".txt"):
            with open(filePath+file,'r') as myfile:
                data = myfile.readlines()
                data = data[1].strip('\n') #stored names in memory,
                                           #could be a class but im lazy
                stored.append(data)
    print(stored)
    return stored

def SelectUser(toolOwner,stored):
    if str(toolOwner) in stored:
        return toolOwner
    
    
def createNewTool():
    toolName = input('> Name: ')
    toolBrand = input('> Brand: ')
    DayRate = input('> Day Rate: ')
    stored = AllUsers()
    toolOwner = input('> Select a Owner: ')
    SelectUser(toolOwner, stored)
    tool = Tool.createTool(toolName, toolBrand,toolOwner,DayRate)
    print('New user with the owner: ' + str(toolOwner) + ' is created.')

def __main__():
    print('1 = Create User')
    print('2 = View all Users')
    print('3 = Create Tool')
    x = input('> ')
    if x == '1':
        createNewUser()
    if x == '2':
        AllUsers()
    if x == '3':
        createNewTool()
    if x == '7':
        pass
    else:
        __main__()
        

__main__()
