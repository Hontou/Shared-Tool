import os
import uuid
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
    def buildFullName(self): # Forename + Surname return#
        return self.user_forename + ' ' + self.user_surname

    #-------------------------------
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
    #-------------------------------
    
    def createUser(userForename, userSurname, userAddress, userEmail, userPassword):
        userId = uuid.uuid4().hex #random id for the user, this will eventually be used
                                  #to identify the user instead of using buildFullName()
        newUser = User(userId, userForename, userSurname, userAddress, userEmail, userPassword)
        newUser.buildFile()
        return userId      
            
      #-------------------------------File/Text Documentation Functions-------------------------------#
    def readFile(self):
        filePath = self.Path()
        fileName = filePath + str(self.user_forename +' '+ self.user_surname)
        with open(fileName + '.txt' , 'r') as myfile:
            data = myfile.readlines()#reads line by line
            #print(data[1])
        
    def buildFile(self): #Builds the .txt file
        filePath = self.Path()
        self.createUserFile(filePath)
        fileName = filePath + '/' + str(self.buildFullName())
        self.writeUTF(fileName)

    def createUserFile(self, filePath):   #Creates a path      
        if not os.path.exists(filePath): #if it doesnt exist  
            os.makedirs(filePath)

    def writeUTF(self, fileName):     #Writing a user file the information required. 
        output_file = open(fileName + '.txt', 'w')
        output_file.write(self.user_id + '\n'
                          + self.user_forename + ' ' + self.user_surname + '\n'
                          + self.user_address + '\n'
                          + self.user_email + '\n'
                          + self.user_password + '\n')
        output_file.close()
        
    def Path(self): #defined path for users
        return 'UserData/'
    #-------------------------------------------------------------------------------------------#
