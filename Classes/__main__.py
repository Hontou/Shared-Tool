from User import *
from Tool import *
from Time import *#
import datetime


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

    availableTimes(x)
    

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
    
               
                       
    

def hireTime():
    #current_time = str(input('What date would you like to start enlisting this item? > DD-MM-YYYY > '))
    #end_time = str(input('When would you like to stop enlisting this tool? DD-MM-YYYY > '))
    start = datetime.datetime.strptime('11-11-1111', "%d-%m-%Y") 
    end = datetime.datetime.strptime('29-11-1111', "%d-%m-%Y")#knocks 1 off the end date
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    dList = []
    for x in date_generated:
        dList.append(x.strftime("%d-%m-%Y"))
    return('\n'.join(dList))




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
