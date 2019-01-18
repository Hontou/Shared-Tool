import tkinter as tk
import tkinter.messagebox as tm
from tkinter import ttk
from tkinter.ttk import Frame, Label, Style
from User import *
from Tool import *
import datetime
import time
import os

LARGE_FONT=("Verdana", 12) #standard font

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
                        
    return '\n'.join(stored[:12])

def grabtemp(x,line):
    f = open("TempData/" + str(x) + ".txt", "r")
    data = f.readlines()
    return data[int(line)]


        
    

##############################################################################################

class SharedPower(tk.Tk): #Initializer

    def __init__(self): #Constructors
        tk.Tk.__init__(self)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand= True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

    
        
        self.frames = {}

        for F in (StartPage, Logged, RegisterPage, RegisterToolPage, SearchToolPage, InvoicePage,ReturnToolPage):
            
            frame = F(container, self)
            
            self.frames[F] = frame
            frame.grid(row=0, column = 0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame): #Main Page

    '''Home Page, all pages has same starting __in__it,
        page contains main login function which stores
        temp login data.'''
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="SharedPower", font=("Verdana", 12))
        label.grid(row=0, column=0, sticky=tk.W)
        Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 9')
        
        #####Login Inputs#####
        username = ttk.Label(self, text="Email")
        username.grid(row=0, column=2, sticky=tk.W)

        username_i = ttk.Entry(self)
        username_i.grid(row=0, column=3, sticky=tk.W)
        password = ttk.Label(self, text="Password")
        password.grid(row=0, column=4, sticky=tk.W)

        password_i = tk.Entry(self)
        password_i.grid(row=0, column=5, sticky=tk.W)
        #####Login Inputs#####
        
        maintext = ttk.Label(self, text="List of Registered Users: ", font=("Verdana", 11))
        emptytext = Label(self, width=20).grid(row=1, column=0)
        maintext.grid(row=2, column=0, sticky=tk.W)   
        subtext = ttk.Label(self, text=AllUsers(), wraplength=500, font='serif 10')
        subtext.grid(row=4, column=0, sticky=tk.W)        
#############################################################################################################################################
        #Main Buttons
        login = ttk.Button(self, text="Log In",
                                command=lambda: logcheck(self, username_i.get(), password_i.get()))#.get username and password from entry   
        login.place(rely=0, relx=1.0, x=0, y=0, anchor=tk.NE)
                              
        button2 = ttk.Button(self, text="Register User",
                             command=lambda: controller.show_frame(RegisterPage))#page redirect
        button2.place(rely=1.0, relx=0, x=0, y=0, anchor=tk.SW)

        button3 = ttk.Button(self, text="Search Tool",
                            command=lambda: controller.show_frame(SearchToolPage))#page redirect
        button3.place(rely=1.0, relx=0, x=86, y=0, anchor=tk.SW)
 
        button4 = ttk.Button(self, text="Create Tool",
                            command=lambda: failedlogin())#needs to log in first
        button4.place(rely=1.0, relx=0, x=170, y=0, anchor=tk.SW)

        button5 = ttk.Button(self, text="Invoice",
                            command=lambda: failedlogin())#needs to log in first
        button5.place(rely=1.0, relx=0, x=255, y=0, anchor=tk.SW)      

        button6 = ttk.Button(self, text="Quit",
                            command=quit)#quit
        button6.place(rely=1.0, relx=1.0, x=0, y=0, anchor=tk.SE)

        button7 = ttk.Button(self, text="Return Tool",
                            command=lambda: failedlogin())#needs to log in first
        button7.place(rely=1.0, relx=0, x=340, y=0, anchor=tk.SW)

#############################################################################################################################################

        def failedlogin():
            tm.showerror("Error", "Please login/register an account before trying to access.")
            controller.show_frame(RegisterPage)
        def logcheck(self, email, password):  #New Login, Displays if username or password wrong with a FOR/IF statement.
            auth = None #Validation for wrong creds
            
            filePath = User.Path('userdata') #Data file to be checked with input
            for file in os.listdir(filePath): #reads all files within the user/data file.
                if file.endswith(".txt"): #making sure to read them all by "txt" files
                    with open(filePath+file,'r') as myfile:
                        data = myfile.readlines() #stores data temporarily inside a var
                        if email == str(data[3].strip('\n')): #compares login with current files data
                            if password == str(data[4].strip('\n')): #compares password with current file data
                                controller.show_frame(Logged) #if correct, relocated to a logged area.
                                auth = True #validation becomes true
                                x = data[0].strip('\n')  #the unique_id is then placed in a variable, detaching itself from the newline key.
                                tm.showinfo("Login","Logged in as:  "+data[1]) #Pop-up showing logged details.
                                if not os.path.exists('TempData/'):
                                    os.makedirs('TempData/') #if file doesnt exist, create it.
                                tempfile = 'TempData/login' 
                                output_file = open(tempfile + '.txt', 'w')
                                output_file.write(data[0]+data[1]+data[2]+data[3]+data[4])#this section writes the logged users information
                                output_file.close() #into a temporary storage to be called while program still active.
                                return data[0]
                            else:
                                auth = False
                        else:
                            auth = False
                                
            if auth is False: #validation error
                tm.showerror("Error", "Wrong Username or Password")#error Message
                              
  
        
    
class Logged(tk.Frame):
    '''Initialises, Logged in page.
       Page allows access to createTool,
       Invoice and return'''
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        token = Logged.grabtoken() 
        loggedtext = ttk.Label(self, text='Currently Logged in')
        loggedtext.grid(row=0, column=5, sticky=tk.E)

        label = ttk.Label(self, text="SharedPower", font=("Verdana", 12))
        label.grid(row=0, column=0, sticky=tk.W)
        Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 9')

        maintext = ttk.Label(self, text="List of Registered Users: ", font=("Verdana", 11))
        emptytext = Label(self, width=20).grid(row=1, column=0)
        maintext.grid(row=2, column=0, sticky=tk.W)   
        subtext = ttk.Label(self, text=AllUsers(), wraplength=500, font='serif 10')
        subtext.grid(row=4, column=0, sticky=tk.W)      
        
        def logout(): #Function for logging out button1
            controller.show_frame(StartPage)
            Logged.deletetoken()
        
        button1 = ttk.Button(self, text="Log Out",
                            command=lambda: logout())#log out and redirects to main
        button1.place(rely=0, relx=1.0, x=0, y=0, anchor=tk.NE) 
        button2 = ttk.Button(self, text="Register User",
                             command=lambda: controller.show_frame(RegisterPage))#page redirect
        button2.place(rely=1.0, relx=0, x=0, y=0, anchor=tk.SW)
        button3 = ttk.Button(self, text="Search Tool",
                            command=lambda: controller.show_frame(SearchToolPage))#page redirect
        button3.place(rely=1.0, relx=0, x=86, y=0, anchor=tk.SW)
        button4 = ttk.Button(self, text="Invoice",
                            command=lambda: controller.show_frame(InvoicePage))#page redirect
        button4.place(rely=1.0, relx=0, x=255, y=0, anchor=tk.SW)
        button5 = ttk.Button(self, text="Create Tool",
                            command=lambda: controller.show_frame(RegisterToolPage))#page redirect
        button5.place(rely=1.0, relx=0, x=170, y=0, anchor=tk.SW)      
        button6 = ttk.Button(self, text="Quit",
                            command=quit)#quit
        button6.place(rely=1.0, relx=1.0, x=0, y=0, anchor=tk.SE)
        button7 = ttk.Button(self, text="Return Tool",
                            command=lambda: controller.show_frame(ReturnToolPage))#page redirect
        button7.place(rely=1.0, relx=0, x=340, y=0, anchor=tk.SW)

    def grabtoken(): #Method of opening the temp log file.
            stored = []
            start_counter = 0
            for file in os.listdir('TempData/'):
                if file.endswith('.txt'):
                    with open('TempData/'+file, 'r') as myfile:
                            data = myfile.readlines()
                            while start_counter < 4:
                                stored.append(data[start_counter].strip('\n'))
                                start_counter = start_counter + 1
                                print(stored[start_counter])
                    return stored

    def deletetoken(): #deletes upon log out
        filePath ='TempData/'
        for file in os.listdir(filePath):
            if file.endswith('.txt'):
                os.remove(filePath+file)            

class InvoicePage(tk.Frame):
    
    '''Invoice Page allows search of each month and year combo,
        returns a invoice of that timeframe in a listbox form.'''
    
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self,parent)
        label = ttk.Label(self, text="SharedPower Invoice", font=("Verdana", 12))
        label.grid(row=0, column=0, sticky=tk.W)
        Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 9')
        def backtologged():
            try:
                f = open('TempData/login.txt')
                f.close()
                controller.show_frame(Logged)
            except FileNotFoundError:
                controller.show_frame(StartPage)

        
        button1 = ttk.Button(self, text="Back to Main",
                            command=lambda: backtologged())#redirect page
        button1.place(rely=0, relx=1.0, x=0, y=0, anchor=tk.NE)
        button2 = ttk.Button(self, text="Quit",
                            command=quit)#quit
        button2.place(rely=1.0, relx=1.0, x=0, y=0, anchor=tk.SE)

        emptybox = ttk.Label(self, text="")#empty grid fillers
        emptybox.grid(row=1, column=0)#empty grid fillers

        monthlabel = ttk.Label(self, text="Month of Invoice")
        monthlabel.grid(row=2, column=0)
        yearlabel = ttk.Label(self, text="Year of Invoice")
        yearlabel.grid(row=2, column=1)   
        month = tk.StringVar(self)
        month.set("Month")
        monthbox = tk.OptionMenu(self, month, "01", "02", "03",
                       "04", "05", "06",
                       "07", "08", "09",
                       "10", "11", "12")
        monthbox.grid(row=3, column=0, sticky=tk.W)  
        year = tk.StringVar(self)
        year.set("Year")
        yearbox = tk.OptionMenu(self, year, "2019", "2020", "2021",
                       "2022", "2023", "2024", "2025")
        yearbox.grid(row=3, column=1)
        
        
        produce_invoice = ttk.Button(self, text="Produce Invoice",
                                     command=lambda: invoice(month.get(),year.get()))  
        produce_invoice.place(rely=1.0, relx=0, x=0, y=0, anchor=tk.SW)


        def invoice(month, year):
            check_month = isinstance(int(month), int)
            check_year = isinstance(int(year), int)
            if check_month == True and check_year == True:
                f = open('TempData/login.txt', "r")
                login_data = f.readlines()
                f.close()

                hireTools = []
                tempL = []
                allTool = []
                hireCost = []
                finalCost = []
                count = 0
                user_id = login_data[0].replace("\n", "")
                tMY = str(month) + "-" + str(year)
                print(tMY)
                f=open("UserData/" + user_id + ".txt", "r")
                for line in f:
                    if "!" in line:
                        if tMY in line:
                            l = line.replace("\n", "")
                            splitO = l.split("!")
                            tool = splitO[0]
                            datePrice = splitO[1].split("£")
                            tempL.append([tool, datePrice[1]])
                            allTool.append(tool)
                f.close 

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

                f = open("UserData/" + user_id + ".txt", "r")
                data = f.readlines()
                f.close

                grandTot = 0
                count = 0
                for line in hireTools:
                    grandTot = grandTot + finalCost[count]
                    count += 1
                grandTot = grandTot + int(data[5].replace("\n", ""))
                count = 0
                
                f=open("InvoiceData/" + month + year + user_id + ".txt", "w")
                f.writelines(data[2].replace("\n", "") + "'s invoice of month " + month + " in year " + year)
                f.writelines("\nTool Hire Charges:\n")
                for line in hireTools:
                    f.writelines(hireTools[count] + " £" + str(finalCost[count]) + "\n")
                    count += 1
                f.writelines("\nDelivery Costs:\n£" + data[5])
                f.writelines("Subtotal:\n£" + str(grandTot) + "\n")
                f.writelines("Additional Insurance Cost: £5\n")
                grandTot += 5
                f.writelines ("Grand Total:\n£" + str(grandTot))
                f.close()
                f=open("InvoiceData/" + month + year + user_id + ".txt", "r")
                data = f.readlines()
                listbox = tk.Listbox(self, width=40, height=12)
                listbox.grid(row=4, column=2)
                for i in  reversed(data):
                    listbox.insert(0, i.replace("\n", ""))
                f.close()
            else:
                tm.showerror("Error", "Please enter a value.")
                controller.show_frame(InvoicePage)
            
            

        
class SearchToolPage(tk.Frame):
    
    '''Search Tool Page, allows for search by tool name,
       Shows a list within a listbox and allows for more information to be shown.
        This will then show booking available dates and allows for booking.
        Bookings are done via appending details of the booking to the tool.'''
    
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self,parent)
        label = ttk.Label(self, text="SharedPower Search", font=("Verdana", 12))
        label.grid(row=0, column=0, sticky=tk.W)
        Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 9')

        def backtologged(): #Repetitive Function that checks for logged or not, returns to corrosponding page.
            try:
                f = open('TempData/login.txt') #checks existence of a login file, in theory if it isnt available you are not logged in and thus returned.
                f.close()
                controller.show_frame(Logged)
            except FileNotFoundError:
                controller.show_frame(StartPage)
                
        emptytext = ttk.Label(self, text="")
        emptytext.grid(row=2,column=0)
        maintext = ttk.Label(self, text="Search Input:", font=("Verdana", 10))
        maintext.grid(row=3, column=0, sticky=tk.W)   
        search_entry = tk.Entry(self,width=40)
        search_entry.grid(row=4, column=0, sticky=tk.W) #entry box for search
        search_button = ttk.Button(self,text="Search",
                                  command= lambda: searchtool(search_entry.get())) #Search tool function followed which takes the entry above
        search_button.grid(row=4, column=1, sticky=tk.W)
        emptytext = ttk.Label(self, text="")
        emptytext.grid(row=5,column=0)
        listbox = tk.Listbox(self,width=40)
        listbox.grid(row=6,column=0)#listbox to fill for later within searchtool() function


        moreinfo_search = ttk.Button(self, text="More Information",
                                     command= lambda: selectactive(listbox.get(tk.ACTIVE)))#can only be used after a tool is selected from the listbox above. Linked to selectactive function.
        moreinfo_search.grid(row=6, column=1)
        
        button1 = ttk.Button(self, text="Back to Main",
                            command=lambda: backtologged())
        button1.place(rely=0, relx=1.0, x=0, y=0, anchor=tk.NE)
      
        button2 = ttk.Button(self, text="Quit",
                            command=quit)
        button2.place(rely=1.0, relx=1.0, x=0, y=0, anchor=tk.SE)
        
        def searchtool(x):
            listbox.delete(0, tk.END)#deletes upon refresh to allow for multiple searches.
            x=x.lower()#caps lower
            filePath = Tool.Path('tooldata')
            storedtools = []
            f = open(filePath + "ToolDir" + ".txt", "r")#toolDir is an easier accesspoint for looking through the list of available tools.
            data = f.readlines()
            f.close()
            for line in data:
                if x in line:
                    listbox.insert(0, line.replace('\n', ''))#fills listbox with all available tools with input name.
            
        def selectactive(x):#input from listbox
            tool_file = open(Tool.Path('tooldata') + str(x) + ".txt", "r")#searches for toolfile with inputname
            tool_data = tool_file.readlines()#stores said tool
            tool_file.close()
            if not os.path.exists('TempData/'):
                os.makedirs('TempData/')#preparing to store the tool temp file.
            tempfile = 'TempData/activetool'
            output_file = open(tempfile + '.txt', 'w')
            output_file.writelines(tool_data)#writes tempfile for activetool.
            output_file.close()
            try:
                f = open('TempData/login.txt')
                user_id = f.readlines()
                f.close()
                myfile = open('TempData/activetool.txt', 'r')
                data = myfile.readlines()

                '''Writes the tool information out in one line of the program.'''
                
                toolInfo = tk.Label(self,text='Tool Name: {0} | Tool Brand: {1}\n'.format(data[0].replace("\n", ""),
                                                                                          data[1].replace("\n", "")) +
                                    'Hire Cost: {0} | Tool Owner: {1}'.format(data[2].replace("\n", ""),
                                                                                          ownerInformation(data[3]).replace("\n", "")))

                temp = []
                for item in data:
                    if "2019 " in item:
                        temp.append(item.replace(" \n", ""))#not future proofed as of yet, 2019 and 2020 only.
                    elif "2020 " in item:
                        temp.append(item.replace(" \n", ""))
                        
                listofdays = tk.StringVar(self)
                listofdays.set(temp[0])
                listofdays.set("Booking Start Date")
                toolInfo.grid(row=4, column=4)
                startdate = tk.OptionMenu(self, listofdays, *temp)
                startdate.grid(row=5, column=4, sticky=tk.W)
                booking_var = tk.StringVar(self)
                booking_var.set(temp[0])
                booking_var.set("Booking End Date")
                bookAmount = tk.OptionMenu(self, booking_var, *temp)
                bookAmount.place(rely=1, relx=1.0, x=-30, y=-204, anchor=tk.NE)
                submit_button = ttk.Button(self, text="Submit",command=lambda: dateListGen(listofdays.get(), booking_var.get(), user_id[0], x)) 
                submit_button.place(rely=1.0, relx=1.0, x=-60, y=0, anchor=tk.SE)

                def dateListGen(start, end, user_id, tool_id):
                    start = start.replace(" ", "")
                    end = end.replace(" ", "")
                    start = datetime.datetime.strptime(start, "%d-%m-%Y")
                    end = datetime.datetime.strptime(end, "%d-%m-%Y")
                    trueEnd = (end-start).days + 1
                    startEnd = [start + datetime.timedelta(days=x) for x in range(0, trueEnd)]
                    seList = []
                    for x in startEnd:
                        seList.append(x.strftime("%d-%m-%Y"))
                    day(seList, user_id, tool_id)
                    
                def day(date_list, user_id, tool_id):
                    user_id = user_id.replace("\n", "")
                    tool_id = tool_id.replace("\n", "")
                    f=open("UserData/" + user_id + ".txt", "r")
                    userTStore = f.readlines()
                    f.close
                    f=open("ToolData/" + tool_id + ".txt", "r")
                    data = f.readlines()
                    f.close
                    f=open("ToolData/" + tool_id + ".txt", "r")
                    tempStore = []
                    count = 0
                    oor = len(date_list) - 1
                    for line in f:
                        ID = date_list[count]
                        if not ID in line:
                            tempStore.append(line)
                        if ID in line:
                            tempStore.append(ID + "#" + user_id + "$Hired\n")
                            userTStore.append(tool_id + "!" + ID + "£" + data[2])
                            if count < oor:
                                count += 1
                    f.close
                    f=open("ToolData/" + tool_id + ".txt", "w")
                    f.writelines(tempStore)
                    f.close
                    f=open("UserData/" + user_id + ".txt", "w")
                    f.writelines(userTStore)
                    f.close
                    tm.showinfo("Booked", "Tool has been hired to user: "+ user_id)
                    controller.show_frame(Logged)
                    
                #def addDelCost(userID):
                #    f=open("UserData/" + userID + ".txt", "r")
                #    data = f.readlines()
                #    f.close
                #    delLoc = data[5].replace("\n", "")
                #    delLoc = int(delLoc) + 5
                #    data[5] = str(delLoc) + "\n"
                #    f=open("UserData/" + userID + ".txt", "w")
                #    f.writelines(data)
                #    f.close

                #def transferMethod():
                #    f=open("TempData/login.txt", "r")
                #    lData = f.readlines()
                #    f.close
                #    user = lData[0].replace("\n", "")
                #    f=open("TempData/activetool.txt", "r")
                #    tData = f.readlines()
                #    f.close
                #    tool = tData[0].replace("\n", "")
                #    delivery = tm.askyesno("Delivery Choice", "Do you want this item delivered? There will be an additional £5 charge", icon='warning')
                #    if delivery == False:
                #        f=open("ToolData/" + tool + ".txt", "r")
                #        tTool_data = f.readlines()
                #        tOwner = tTool_data[3].replace("\n", "")
                #        f.close#
                #
                #                        f=open("UserData/" + tOwner + ".txt", "r")
                #        tUser_data = f.readlines()
                #        tAddress = tUser_data[2]
                #        f.close
                #        tm.showinfo("Location","The Pick Up Location is:  " +tAddress)
                #            
                #    if delivery ==True:
                #        print(user)
                #        with open("UserData/"+user+".txt") as f:
                #        #f=open("UserData/"+user+".txt")
                #            data = list(f)
                #            print(data)
                #            f.close()
                # 
                        #booker = dataList[2].replace("\n", "")
                        #addDelCost(user)
                        #tm.showinfo("Location","Thank you for your order, the " + tool + " will be delivered to your address of: " + booker)
                        #controller.show_frame(Logged)

         
            except FileNotFoundError:
                tm.showerror("Error", "Please login to access this page.")
                controller.show_frame(StartPage)
    
            
        def ownerInformation(user_id):
            f = open('UserData/'+ user_id.replace("\n", "") + '.txt')
            data = f.readlines()
            return data[1]

            


  


        
class RegisterToolPage(tk.Frame):
    
    '''Registration of Tools, requires nothing.
       Reads through tool class file and takes the create tool function with parameters'''
    
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Logged In", font=LARGE_FONT)
        label.place
        label = ttk.Label(self, text="SharedPower Registration", font=("Verdana", 12))
        label.grid(row=0, column=0, sticky=tk.W)
        Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 9')

        def backtologged(): #Repetitive Function that checks for logged or not, returns to corrosponding page.
            try:
                f = open('TempData/login.txt') #checks existence of a login file, in theory if it isnt available you are not logged in and thus returned.
                f.close()
                controller.show_frame(Logged)
            except FileNotFoundError:
                controller.show_frame(StartPage)
        
        button1 = ttk.Button(self, text="Back to Main",
                            command=lambda:backtologged()) #main page via log checker
        button1.place(rely=0, relx=1.0, x=0, y=0, anchor=tk.NE)     
        button6 = ttk.Button(self, text="Quit",
                            command=quit)#quit
        button6.place(rely=1.0, relx=1.0, x=0, y=0, anchor=tk.SE)
        
        maintext = ttk.Label(self, text="Tool Registration Form: ", font=("Verdana", 11))
        emptytext = Label(self, width=20).grid(row=1, column=0)
        maintext.grid(row=2, column=0, sticky=tk.W)
 
        toolname = ttk.Label(self, text="Tool Name")
        toolname.grid(row=4, column=0, sticky=tk.W)
        toolname_i = ttk.Entry(self)#tool register input [tool name]
        toolname_i.grid(row=5, column=0, sticky=tk.W)

        toolbrand = ttk.Label(self, text="Tool Brand")
        toolbrand.grid(row=6, column=0, sticky=tk.W)
        toolbrand_i = tk.Entry(self)#tool register input [tool brand]
        toolbrand_i.grid(row=7, column=0, sticky=tk.W)

        dayrate = ttk.Label(self, text="Day Rate")
        dayrate.grid(row=8, column=0, sticky=tk.W)
        dayrate_i = tk.Entry(self)#tool register input [day rate]
        dayrate_i.grid(row=9, column=0, sticky=tk.W)

        start = ttk.Label(self, text="Start Date")
        start.grid(row=4, column=1, sticky=tk.W)
        start_i = tk.Entry(self)#tool register input [start date]
        start_i.grid(row=5, column=1, sticky=tk.W)
        warning_start = ttk.Label(self, text="Input format as DD-MM-YYYY")
        warning_start.grid(row=5,column=2, sticky=tk.W)
        
        end = ttk.Label(self, text="End Date")
        end.grid(row=6, column=1, sticky=tk.W)
        end_i = tk.Entry(self)#tool register input [end date]
        end_i.grid(row=7, column=1, sticky=tk.W)
        warning_end = ttk.Label(self, text="Input format as DD-MM-YYYY")
        warning_end.grid(row=7,column=2, sticky=tk.W)

        submit = ttk.Button(self, text="Submit",
                            command=lambda: createNewTool(toolname_i.get(), toolbrand_i.get(),
                                                          dayrate_i.get(), start_i.get(),
                                                          end_i.get()))#.get parameters from listed entries above. 
        submit.grid(row=8, column=1, sticky=tk.W)
        
        def createNewTool(toolname, toolbrand, dayrate, start, end): #function mostly comprised of taking function from Tools.py
            start = datetime.datetime.strptime(start, "%d-%m-%Y") #reformats date for use
            end = datetime.datetime.strptime(end, "%d-%m-%Y") #reformats date for use
            trueEnd = (end-start).days + 1 #generates a true end to calculate days inbetween start/end
            token = grabtemp('login', 0)#function from outside allows for quick user_id
            date_generated = [start + datetime.timedelta(days=x) for x in range(0, trueEnd)]#true end continued.
            dList = []
            for x in date_generated:
                dList.append(x.strftime("%d-%m-%Y"))#appends all days listed.
            nList = (' \n'.join(dList))#newline for each entry
            tool = Tool.createTool(toolname.lower(), toolbrand.lower(),token,dayrate,nList)#creates the file + tool object/file
            #print('New tool with the owner: ' + str(token) + ' is created.')
            filePath = User.Path('userdata') #this plus for statement below appens tool to owner.
            for file in os.listdir(filePath):
                if file.startswith(str(token)):
                    with open(filePath+file, 'a') as myfile:
                        myfile.write(str(tool+"\n"))
            f = open("ToolData/ToolDir.txt", "a+") #adds tool to directory for future accessibility
            f.write(toolname + "\n")
            f.close
            tm.showinfo("Created", "Tool has been created")
            controller.show_frame(Logged)#redirects page
            

            
class RegisterPage(tk.Frame): #Logged In Page
    
    '''User registration page, slightly the same as page above'''
    
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Logged In", font=LARGE_FONT)
        label.place
        label = ttk.Label(self, text="SharedPower Registration", font=("Verdana", 12))
        label.grid(row=0, column=0, sticky=tk.W)
        Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 9')

        def backtologged(): #Repetitive Function that checks for logged or not, returns to corrosponding page.
            try:
                f = open('TempData/login.txt') #checks existence of a login file, in theory if it isnt available you are not logged in and thus returned.
                f.close()
                controller.show_frame(Logged)
            except FileNotFoundError:
                controller.show_frame(StartPage)

        button1 = ttk.Button(self, text="Back to Main",
                            command=lambda:backtologged())#back to main via above function
        button1.place(rely=0, relx=1.0, x=0, y=0, anchor=tk.NE)      
        button6 = ttk.Button(self, text="Quit",
                            command=quit)#quit
        button6.place(rely=1.0, relx=1.0, x=0, y=0, anchor=tk.SE)
        
        maintext = ttk.Label(self, text="Registration Form: ", font=("Verdana", 11))
        emptytext = Label(self, width=20).grid(row=1, column=0)
        maintext.grid(row=2, column=0, sticky=tk.W)

        forename = ttk.Label(self, text="Forename")
        forename.grid(row=4, column=0, sticky=tk.W)
        forename_i = ttk.Entry(self)# [forename]
        forename_i.grid(row=5, column=0, sticky=tk.W)

        surname = ttk.Label(self, text="Surname")
        surname.grid(row=6, column=0, sticky=tk.W)
        surname_i = tk.Entry(self)# [surname]
        surname_i.grid(row=7, column=0, sticky=tk.W)

        address = ttk.Label(self, text="Post Code")
        address.grid(row=8, column=0, sticky=tk.W)
        address_i = tk.Entry(self)# [address]
        address_i.grid(row=9, column=0, sticky=tk.W)

        email = ttk.Label(self, text="Email")
        email.grid(row=4, column=1, sticky=tk.W)
        email_i = ttk.Entry(self)# [email]
        email_i.grid(row=5, column=1, sticky=tk.W)

        password = ttk.Label(self, text="Password")
        password.grid(row=6, column=1, sticky=tk.W)
        password_i = ttk.Entry(self)# [passwprd]
        password_i.grid(row=7, column=1, sticky=tk.W)
        

        submit = ttk.Button(self, text="Submit",
                            command=lambda: createNewUser(forename_i.get(), surname_i.get(),
                                                          address_i.get(), email_i.get(),
                                                          password_i.get()))#.get  parameters from entries above  
        submit.grid(row=9, column=1, sticky=tk.W)
        
        def createNewUser(userForename, userSurname, userAddress, userEmail, userPassword): #Creates account with User class.
            counter = 0 #validation counter
            listoflist = [userForename, userSurname, userAddress, userEmail, userPassword] #stores parameters in list
            val = 0 #validation for parameter input.
            while counter < 5:
                if listoflist[counter] == '':
                    pass
                else:
                    val = val + 1
                
                counter = counter + 1

            if val == 5:
                user = User.createUser(userForename, userSurname, userAddress,userEmail,userPassword) #Classes/User
                controller.show_frame(StartPage)
                tm.showinfo("Registered", "You can now Login.")#once created, popup of creation and returns to main page
            else:
                tm.showerror("Error", "Parameter(s) not entered.")#wrong parameters

        
class ReturnToolPage(tk.Frame):
    
    '''Returns tool via currently owned tools'''
    
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        
        label = ttk.Label(self, text="SharedPower Return", font=("Verdana", 12))
        label.grid(row=0, column=0, sticky=tk.W)
        Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 9')

        def backtologged(): #Repetitive Function that checks for logged or not, returns to corrosponding page.
            try:
                f = open('TempData/login.txt') #checks existence of a login file, in theory if it isnt available you are not logged in and thus returned.
                f.close()
                controller.show_frame(Logged)
            except FileNotFoundError:
                controller.show_frame(StartPage)
        

        button1 = ttk.Button(self, text="Back to Main",
                            command=lambda:backtologged())#back to main page or logged via function above
        button1.place(rely=0, relx=1.0, x=0, y=0, anchor=tk.NE)     
        button6 = ttk.Button(self, text="Quit",
                            command=quit)#quit
        button6.place(rely=1.0, relx=1.0, x=0, y=0, anchor=tk.SE)
        
        emptytext = ttk.Label(self, text="")
        emptytext.grid(row=2,column=0)
        maintext = ttk.Label(self, text="Search Input:", font=("Verdana", 10))
        maintext.grid(row=3, column=0, sticky=tk.W)   
        search_entry = tk.Entry(self,width=40)# [search entry for currently owned]
        search_entry.grid(row=4, column=0, sticky=tk.W)
        search_button = ttk.Button(self,text="Search",
                                  command= lambda: searchhiredtool(search_entry.get()))#searchhire function, repeated from search function within search page.
        search_button.grid(row=4, column=1, sticky=tk.W)
        emptytext = ttk.Label(self, text="")
        emptytext.grid(row=5,column=0)
        listbox = tk.Listbox(self,width=30)
        listbox.grid(row=6,column=0)
        
        moreinfo_search = ttk.Button(self, text="Remove Item",
                                     command= lambda: returnItem(listbox.get(tk.ACTIVE)))#item return takes listbox input
        moreinfo_search.grid(row=6, column=1)

        
        def searchhiredtool(search_entry):
            
            '''Check first searchtool above page, reposted function'''
            
            listoffoundtools = []
            startingline = 0
            listbox.delete(0, tk.END)
            search_entry=search_entry.lower()
            filePath = User.Path('userdata')
            storeduser = grabtemp('login',0)
            f = open(filePath + storeduser.replace("\n", "") + ".txt", "r")
            data = f.readlines()
            f.close()
            
            for line in data:
                if line in (line for line in data if not line.startswith('[')):
                    if "!" in line:
                        splitter = line.split("!")
                        if splitter[0] not in listoffoundtools:
                            listoffoundtools.append(splitter[0])
                            listbox.insert(0, splitter[0])
                else:
                    pass

        def returnItem(item): #input from listbox
            storeduser = grabtemp('login',0)#grabs current user which in turn allows for location of actual file
            f=open("UserData/" + storeduser.replace("\n", "") + ".txt", "r")
            user_data = f.readlines()#stores actual file into variable
            f.close
            filterS = item + "!" #filters for any owned item and appends a returned to that item.
            cTool = [item]
            allDat = []
            for line in user_data:
                if filterS in line:
                    allDat.append("[Returned]" + line)
                    eSplit = line.split("!")
                    pSplit = eSplit[1]
                    date = pSplit.split("£")
                    cTool.append(date[0])

            f=open("UserData/" + storeduser.replace("\n", "") + ".txt", "w")
            count = 0
            for line in user_data:
                if not filterS in line:
                    f.writelines(line)
                if filterS in line:
                    f.writelines(allDat[count])
                    count += 1
                    
            printStr = ""
            counter = 0
            for i in cTool:
                printStr = printStr + "\n" + str(cTool[counter])
                counter += 1
            tm.showinfo("Removed", "These are removed dates for: "+printStr)
            controller.show_frame(Logged)
            
                
            
            

Logged.deletetoken()

def __main__():
    app = SharedPower()#app run
    app.geometry("620x300")
    app.resizable(0, 0)
    app.mainloop()#loop

__main__()
