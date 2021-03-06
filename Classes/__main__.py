from User import *
from Tool import *
from Time import *#
import datetime



#REMOVE

def login():
    email = 'micharin99@gmail.com'
    password = '1234'
    filePath = User.Path('userdata')
    for file in os.listdir(filePath):
        if file.endswith(".txt"):
            with open(filePath+file,'r') as myfile:
                data = myfile.readlines()
                if str(email) == str(data[3].strip('\n')):
                    if str(password) == str(data[4].strip('\n')):
                        print('logged')
                        return data[0]
                    
                    
def createNewUser():
    userForename = input('> Forename: ')
    userSurname = input('> Surname: ')
    userAddress = input('> Address: ')
    userEmail = input('> Email: ')
    userPassword = input('> Password: ')
    user = User.createUser(userForename, userSurname, userAddress,userEmail,userPassword)
    print('New user with id: ' + user + ' created.')


def createNewTool(token):
    toolName = input('> Name: ')
    toolBrand = input('> Brand: ')
    DayRate = input('> Day Rate: ')
    bookD = hireTime()
    tool = Tool.createTool(toolName, toolBrand,token,DayRate,bookD)
    print('New tool with the owner id: ' + str(token) + ' is created.')
    filePath = User.Path('userdata')
    for file in os.listdir(filePath):
        if file.startswith(str(token)):
            with open(filePath+file, 'a') as myfile:
                myfile.write(str(tool+"\n"))
    f = open("ToolData/ToolDir.txt", "a+")
    f.write(toolName + "\n")
    f.close
        

    
        
def listofownedTools(token):
    stored = []
    start_counter = 5
    filePath = User.Path('userdata')
    for file in os.listdir(filePath):
        if file.startswith(str(token)):
            num_lines = sum(1 for line in open(filePath+file)) -1
            with open(filePath+file, 'r') as myfile:
                        data = myfile.readlines()
                        while start_counter <= num_lines:
                            stored.append(data[start_counter].strip('\n'))
                            start_counter = start_counter + 1
    return stored



def removeTool(token):
    toolsowned = listofownedTools(token)
    userpath = str(User.Path('userdata')+token+'.txt')
    print(', '.join(toolsowned))
    selection = str(input('Which of these tools would you like to delete  > '))
    filePath = Tool.Path('tooldata')
    for file in os.listdir(filePath):
        if file.startswith(str(selection)):
            os.remove(filePath+file)
            with open(userpath, 'r') as myfile:
                lines = myfile.readlines()
                myfile.close()
                myfile = open(userpath, 'w')
                for line in lines:
                    if line!=selection+"\n":
                        myfile.write(line)
                myfile.close()
                print('Item Removed')
        else:
            pass

    

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
    #Copying User Info
    userTStore = []
    userAdd = "UserData/" + userID + ".txt"
    f = open(userAdd, "r")
    for line in f:
        userTStore.append(line)
    f.close
    f = open(addID, "r")
    data = f.readlines()
    f.close
    f = open(addID, "r")
    tempStore = []
    count = 0
    oor = len(identify) - 1
    
    for line in f:
        ID = identify[count]
        if not ID in line:
            tempStore.append(line)
        if ID in line:
            tempStore.append(ID + "#"+ userID + "$Hired" + "\n")
            userTStore.append(fileN + "!" + ID + "£" + data[2])
            if count < oor:
                count+=1
    f.close()
    f = open(addID, "w")
    f.writelines(tempStore)
    f.close()
    #Add Booked Tool to User File
    f = open(userAdd, "w")
    f.writelines(userTStore)
    f.close()


#Adding Late
def lateAdd(user):
    allTool = []
    userI = []
    x = "!"
    lateID = "£"
    f = open("ToolData/ToolDir.txt", "r")
    for line in f:
        allTool.append(line)
    f.close
    #Opens User File to check dates
    f = open("UserData/" + user + ".txt", "r")
    for line in f:
        if not lateID in line:
            if x in line:
                for tool in allTool:
                    if tool in line:
                        y = line
                        z = y.replace("\n", "")
                        e = z.split("!")
                        cT = getDMY()
                        if e[1] < cT:
                            userI.append(z + "£Late" + "\n")
            if not x in line:
                userI.append(line)
        if lateID in line:
            userI.append(line)
    f.close
    f = open("UserData/" + user + ".txt", "w")
    f.writelines(userI)
    f.close
    #Remove and then add a method to write to user file with late fee
#lateAdd("Thomas Law")


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

def addDelCost(Token):
    f = open("UserData/" + Token + ".txt", "r")
    data = f.readlines()
    f.close
    temp = data[5].replace("\n", "")
    temp = int(temp) + 5
    data[5] = str(temp) + "\n"
    f = open("UserData/" + Token + ".txt", "w")
    f.writelines(data)
    
def hireTool(tool, Token):
    print("The following days are available:")
    checkDate = "ToolData/" + tool +".txt"
    f = open(checkDate, "r")
    tempStore = []
    for line in f:
        #2019+2020
        if "2019 " in line:
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
        print(tOwner)
        f.close
        #using the tool owners ID to find their address
        f = open("UserData/" + tOwner + ".txt", "r")
        data = f.readlines()
        print(data)
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
            addDelCost(Token)
            print("Thank you for your order, the " + tool + " will be delivered to " + bookee)
        elif dCheck =="n":
            print("")

#hireTool("Testtt", "Thomas Law")





def sep():
    return "**************************************************\n"

def invoiceGen(userID):
    x = datetime.datetime.now()
    cMonth = x.strftime("%m")
    
    hireTools = []
    tempL = []
    allTool = []
    hireCost = []
    finalCost = []
    count = 0
    
    f = open("UserData/" + userID + ".txt", "r")
    for line in f:
        if "!" in line:
            l = line.replace("\n", "")
            splitO = l.split("!")
            tool = splitO[0]
            datePrice = splitO[1].split("£")
            tempL.append([tool, datePrice[1]])
            allTool.append(tool)
    f.close
    
    
    #Getting it down to just the tool names
    for x in tempL:
        tool = x[0]
        cost = x[1]
        if tool not in hireTools:
            hireTools.append(tool)
            hireCost.append(cost)
    toolQuanDict = {i:allTool.count(i) for i in allTool}    
    
    while count < len(hireTools):
        x = int(toolQuanDict[hireTools[count]]) * int(hireCost[count])
        finalCost.append(x)
        count += 1
    

    f = open("UserData/" + userID + ".txt", "r")
    data = f.readlines()
    f.close
    
    grandTot = 0
    count = 0 
    for line in hireTools:
        grandTot = grandTot + finalCost[count]
        count +=1
    grandTot = grandTot + int(data[5].replace("\n", ""))
    
    count = 0
    
    f = open("InvoiceData/" + cMonth + userID + ".txt", "w")
    f.writelines("\n" + sep() + "\n")
    f.writelines(userID + "'s invoice of month " + cMonth + "\n")
    f.writelines("\n" + sep() + "\n")
    f.writelines("Tool Hire Charges:\n")
    for line in hireTools:
        f.writelines(hireTools[count] + " : £" + str(finalCost[count]) + "\n")
        count += 1
    f.writelines("\nDelivery Costs:\n£" + data[5])
    f.writelines("\n" + sep() + "\n")
    f.writelines("Subtotal:\n£" + str(grandTot) + "\n")
    f.writelines("Insurance Monthly Cost: +£5\n")
    grandTot += 5
    f.writelines("\n" + sep() + "\n")
    f.writelines("Grand Ttotal:\n£" + str(grandTot) + "\n")
    f.close

#invoiceGen("Thomas Law")


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
    print('6 = Remove a Tool')
    x = input('> ')
    if x == '1':
        createNewUser()
    if x == '2':
        AllUsers()
    if x == '3':
        createNewTool(token)
    if x == '4':
        searchTool()
    if x == '5':
        token = login()
        return token
    if x == '6':
        removeTool(token)
    if x == '7':
        pass
    else:
        __main__()
        



#token = __main__()
