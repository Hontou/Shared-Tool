from User import *
from Tool import *
from Time import *#

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
    #temp
    tempYesNo = input('> Add unavailable days? ')#
    if tempYesNo == 'Y':#
        bookD = addToolDates()##
    else:#
        bookD = ''#
    temp = AllUsers()#
    toolOwner = input('> Select a Owner: ')#
    print(bookD)#
    if str(toolOwner) in temp:   
        tool = Tool.createTool(toolName, toolBrand,toolOwner,DayRate,bookD)
        print('New tool with the owner: ' + str(toolOwner) + ' is created.')
    else:
        print('Please try again.')
        createNewTool()

#To Add Unavailable Dates############
def addToolDates():
    dCount = 0
    tDateList=[]
    while dCount == 0:
        bookD1 = str(input('> Enter Date: '))
        bookD2 = str(input('> Enter Close Date: '))
        tDateList.append([bookD1, bookD2])
        userTestt = input("> Would you like to add another unavailable period? (Y/N) ")
        if userTestt == 'Y':
            print("hi")
        else:
            dCount += 1
    return tDateList
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
    x = input('> ')
    if x == '1':
        createNewUser()
    if x == '2':
        AllUsers()
    if x == '3':
        createNewTool()
    if x == '4':
        searchTool()
    if x == '7':
        pass
    else:
        __main__()
        

__main__()
