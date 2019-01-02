import os
import uuid
from Tool import *
class User:
    #---------------------------------------Constructors--------------------------------------#
    def __init__(self, userId, userForename = '', userSurname = '', userAddress = '', userEmail= '', userPassword = ''):
        
        self.user_id = userId
        self.user_forename = userForename
        self.user_surname = userSurname
        self.user_address = userAddress
        self.user_email = userEmail
        self.user_password = userPassword

    def __str__(self):

        var += str(self.user_id) + '\n'
        var += self.user_forename + '\n' + self.user_surname + '\n' + self.user_address + '\n' + self.user_email + '\n' + self.password + '\n'
        return var

    def __repr__(self):

        var += str(self.user_id) + '\n'
        var += self.user_forename + '\n' + self.user_surname + '\n' + self.user_address + '\n' + self.user_email + '\n' + self.password + '\n'
        return var
    #------------------------------------------------------------------------------------------#
    
    #-------------------------------Class Functions--------------------------------------------#
    def buildFullName(self):
        return self.user_forename + ' ' + self.user_surname
    
    def getUserId(self):
        return self.user_id

    def getUserForename(self):
        return self.user_forename
    
    def getUserSurname(self):
        return self.user_surname

    def getUserAddress(self):
        return self.user_address

    def getUserEmail(self):
        return self.user_email
    
    def createUser(userForename, userSurname, userAddress, userEmail, userPassword):
        userId = uuid.uuid4().hex
        newUser = User(userId, userForename, userSurname, userAddress, userEmail, userPassword)
        newUser.buildFile()
        return userId      
            
      #-------------------------------File/Text Documentation Functions-------------------------------#
    def readFile(self):
        filePath = self.Path()
        fileName = filePath + str(self.user_forename +' '+ self.user_surname)
        with open(fileName + '.txt' , 'r') as myfile:
            data = myfile.readlines()
            #print(data[1])
        
    def buildFile(self):
        filePath = self.Path()
        self.createUserFile(filePath)
        fileName = filePath + '/' + str(self.buildFullName())
        self.writeUTF(fileName)

    def createUserFile(self, filePath):          
        if not os.path.exists(filePath):
            os.makedirs(filePath)

    def writeUTF(self, fileName):      
        output_file = open(fileName + '.txt', 'w')
        output_file.write(self.user_id + '\n'
                          + self.user_forename + ' ' + self.user_surname + '\n'
                          + self.user_address + '\n'
                          + self.user_email + '\n'
                          + self.user_password + '\n')
        output_file.close()
        
    def Path(self):
        return 'UserData/'
    #-------------------------------------------------------------------------------------------#

    
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
