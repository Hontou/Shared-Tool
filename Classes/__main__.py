from User import *
from Tool import *
from Time import *#
import datetime

#REMOVE
Token = "Thomas Law"

def login():
    email = 'micharin99@gmail.com'
    password = '1234'
    filePath = User.Path('userdata')
    for file in os.listdir(filePath):
        if file.endswith(".txt"):
            with open(filePath+file,'r') as myfile:
                data = myfile.readlines()
                if email == str(data[3].strip('\n')):
                    if password == str(data[4].strip('\n')):
                        return data[1] 
def createNewUser():
    userForename = input('> Forename: ')
    userSurname = input('> Surname: ')
    userAddress = input('> Address: ')
    userEmail = input('> Email: ')
    userPassword = input('> Password: ')
    user = User.createUser(userForename, userSurname, userAddress,userEmail,userPassword)
    print('New user with id: ' + str(user) + ' created.')


def createNewTool():
    toolName = input('> Name: ')
    toolBrand = input('> Brand: ')
    DayRate = input('> Day Rate: ')
    x = '14-11-1111'
    bookD = hireTime()
    temp = AllUsers()
    toolOwner = input('> Select a Owner: ')
    if str(toolOwner) in temp:   
        tool = Tool.createTool(toolName, toolBrand,toolOwner,DayRate,bookD)
        print('New tool with the owner: ' + str(toolOwner) + ' is created.')
    else:
        print('Please try again.')
        createNewTool()
    

#Rewriting
def availableTimes(x):
    fn = 'ToolData/1.txt'
    f = open(fn)
    output = []
    for line in f:
        if not x in line:
            output.append(line)
    f.close()
    f = open("ToolData/1.txt", "w")
    f.writelines(output)
    f.close()
    
               
#Writing Dates to File
def hireTime():
    start = str(input('What date would you like to start enlisting this item? > DD-MM-YYYY > '))
    end = str(input('When would you like to stop enlisting this tool? DD-MM-YYYY > '))
    start = datetime.datetime.strptime(start, "%d-%m-%Y") 
    end = datetime.datetime.strptime(end, "%d-%m-%Y")
    trueEnd = (end-start).days + 1
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, trueEnd)]
    dList = []
    for x in date_generated:
        dList.append(x.strftime("%d-%m-%Y"))
    return(' \n'.join(dList))


#
#Adding an identifier after booking
def bookIdentifier(identify, fileN, userID):
    addID = "ToolData/" + fileN +".txt"
    f = open(addID, "r")
    tempStore = []
    count = 0
    oor = len(identify) - 1
    for line in f:
        ID = identify[count]
        if not ID in line:
            tempStore.append(line)
        if ID in line:
            tempStore.append(ID + "#"+ userID + "\n")
            if count < oor:
                count+=1
    f.close()
    f = open(addID, "w")
    f.writelines(tempStore)
    f.close()


#Finds all the lines with # in and prints
def testBooked(fileN):
    findID = "ToolData/" + fileN + ".txt"
    x = "#"
    f = open(findID, "r")
    tempStore = []
    for line in f:
        if x in line:
            #should change in future to a more suitable way of showing
            print(line)
    f.close()

def hireTool(tool, Token):
    print("The following days are available:")
    checkDate = "ToolData/" + tool +".txt"
    f = open(checkDate, "r")
    tempStore = []
    for line in f:
        #2019+2020
        if "1111 " in line:
            tempStore.append(line.replace(" \n", ""))
    print(tempStore)
    f.close()
    print("Please use the following format: dd-mm-yyyy")
    start = input("What day would you like to start your booking? ")
    start = datetime.datetime.strptime(start, "%d-%m-%Y")
    end = input("What day would you like to end your booking? ")
    end = datetime.datetime.strptime(end, "%d-%m-%Y")
    seList = []
    trueEnd = (end-start).days + 1
    startEnd = [start + datetime.timedelta(days=x) for x in range(0, trueEnd)]
    for x in startEnd:
        seList.append(x.strftime("%d-%m-%Y"))
    print(seList)
    bookIdentifier(seList, tool, Token)

    #Delivery Option
    method = input("Would you like to pick the " + tool + " in person or arrange a delivery? (p/d) ")
    if method == "p":
        #getting the tool owners ID
        f = open("ToolData/" + tool + ".txt", "r")
        data = f.readlines()
        tOwner = data[3].replace("\n", "")
        f.close
        #using the tool owners ID to find their address
        f = open("UserData/" + tOwner + ".txt", "r")
        data = f.readlines()
        tAddress = data[2]
        f.close
        print("Their address is " +tAddress)
    elif method == "d":
        dCheck = input("You have chosen delivery, this be be an additonal £5 charge. Is that okay? (y/n) ")
        if dCheck == "y":
            #using user ID to find address
            f = open("UserData/" + Token + ".txt", "r")
            data = f.readlines()
            bookee = data[2]
            f.close
            print("Thank you for your order, the " + tool + "will be delivered to " + bookee)
        elif dCheck =="n":
            print("")
    
    
#FIND WAY TO INCLUDE USER ADDRESS
hireTool("rewritetest", Token)


###########
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

    
def searchTool():  #Repetative but works.
    print('What would you like to search by?')
    print('1 = Name')
    print('2 = Brand')
    print('3 = Owner')
    userinput = int(input('> '))

    if userinput == 1:
        secondary_input = input('Name? > ')
        filePath = Tool.Path('tooldata')
        storedtools = []
        for file in os.listdir(filePath):
            if file.startswith(secondary_input):
                with open(filePath+file,'r') as myfile:
                    data = myfile.readlines()
                    data = data[0].strip('\n') #stored names in memory,
                                               #could be a class but im lazy
                    storedtools.append(data)
        print(storedtools)
        print('Which item would you like to see the available time and owner of the tool?')
        thirdinput = str(input('> '))
        if thirdinput in storedtools:
            with open(filePath+thirdinput+'.txt','r') as myfile:
                data = myfile.readlines()
                print('Name:'+data[0].strip('\n'))
                print('Brand:'+data[1].strip('\n'))
                print('Day Rate:'+data[2].strip('\n'))
                print('Tool Owner:'+data[3].strip('\n'))
                print('#############################################')
                print('Placeholder Availability')
                print('#############################################')
                
    if userinput == 2:
        secondary_input = input('Brand? > ')
        filePath = Tool.Path('tooldata')
        storedtools = []
        for file in os.listdir(filePath):
            with open(filePath+file,'r') as myfile:
                data = myfile.readlines()
                if str(secondary_input) == str(data[1].strip('\n')):
                    storedtools.append(data[0].strip('\n'))
        print(', '.join(storedtools))
        print('Which item would you like to see the available time and owner of the tool?')
        thirdinput = str(input('> '))
        if thirdinput in storedtools:
            with open(filePath+thirdinput+'.txt','r') as myfile:
                data = myfile.readlines()
                print('Name:'+data[0].strip('\n'))
                print('Brand:'+data[1].strip('\n'))
                print('Day Rate:'+data[2].strip('\n'))
                print('Tool Owner:'+data[3].strip('\n'))
                print('#############################################')
                print('Placeholder Availability')
                print('#############################################')

    if userinput == 3:
        secondary_input = input('Owner? > ')
        filePath = Tool.Path('tooldata')
        storedtools = []
        for file in os.listdir(filePath):
            with open(filePath+file,'r') as myfile:
                data = myfile.readlines()
                if str(secondary_input) == str(data[3].strip('\n')):
                    storedtools.append(data[0].strip('\n'))
        print(', '.join(storedtools))
        print('Which item would you like to see the available time and owner of the tool?')
        thirdinput = str(input('> '))
        if thirdinput in storedtools:
            with open(filePath+thirdinput+'.txt','r') as myfile:
                data = myfile.readlines()
                print('Name:'+data[0].strip('\n'))
                print('Brand:'+data[1].strip('\n'))
                print('Day Rate:'+data[2].strip('\n'))
                print('Tool Owner:'+data[3].strip('\n'))
                print('#############################################')
                print('Placeholder Availability')
                print('#############################################')
                

    else:
        __main__()
                         
   


def __main__():
    print('1 = Create User')
    print('2 = View all Users')
    print('3 = Create Tool')
    print('4 = Search Tool')
    print('5 = Login')
    x = input('> ')
    if x == '1':
        createNewUser()
    if x == '2':
        AllUsers()
    if x == '3':
        createNewTool()
    if x == '4':
        searchTool()
    if x == '5':
        token = login()
        
    if x == '7':
        pass
    else:
        __main__()
        


__main__()
