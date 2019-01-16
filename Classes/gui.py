import tkinter as tk
import tkinter.messagebox as tm
from tkinter import ttk
from tkinter.ttk import Frame, Label, Style
from User import *
from Tool import *
from Time import *

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
    print(data[int(line)])
    return data[int(line)]


        
    

##############################################################################################

class SharedTool(tk.Tk): #Initializer

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


class StartPage(tk.Frame): #Start Page
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Stored Tools", font=("Verdana", 12))
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
#######################################################

        login = ttk.Button(self, text="Log In",
                                command=lambda: logcheck(self, username_i.get(), password_i.get()))#.get username and password from entry   
        login.place(rely=0, relx=1.0, x=0, y=0, anchor=tk.NE)
                              
        
#######################################################  
        button2 = ttk.Button(self, text="Register User",
                             command=lambda: controller.show_frame(RegisterPage))
        button2.place(rely=1.0, relx=0, x=0, y=0, anchor=tk.SW)
#######################################################  
        button3 = ttk.Button(self, text="Search Tool",
                            command=lambda: controller.show_frame(SearchToolPage))
        button3.place(rely=1.0, relx=0, x=86, y=0, anchor=tk.SW)
#######################################################  
        button4 = ttk.Button(self, text="Create Tool",
                            command=lambda: failedlogin())
        button4.place(rely=1.0, relx=0, x=170, y=0, anchor=tk.SW)
#######################################################
        button5 = ttk.Button(self, text="Invoice",
                            command=lambda: failedlogin())
        button5.place(rely=1.0, relx=0, x=255, y=0, anchor=tk.SW)
#######################################################        
        button6 = ttk.Button(self, text="Quit",
                            command=quit)
        button6.place(rely=1.0, relx=1.0, x=0, y=0, anchor=tk.SE)
#######################################################

        def failedlogin():
            tm.showerror("Error", "Please login/register an account before trying to access.")
            controller.show_frame(RegisterPage)
        def logcheck(self, email, password):  #New Login taken from __main__. Displays if username or password wrong with a FOR/IF statement.
            auth = None
            
            filePath = User.Path('userdata')
            for file in os.listdir(filePath):
                if file.endswith(".txt"):
                    with open(filePath+file,'r') as myfile:
                        data = myfile.readlines()
                        if email == str(data[3].strip('\n')):
                            if password == str(data[4].strip('\n')):
                                #print('Logged in as '+data[1])
                                controller.show_frame(Logged)
                                auth = True
                                x = data[0].strip('\n')
                                tm.showinfo("Login","Logged in as:  "+data[1])
                                if not os.path.exists('TempData/'):
                                    os.makedirs('TempData/')
                                tempfile = 'TempData/login'
                                output_file = open(tempfile + '.txt', 'w')
                                output_file.write(data[0]+data[1]+data[2]+data[3]+data[4])
                                output_file.close()
                                return data[0]
                            else:
                                auth = False
                        else:
                            auth = False
                                
            if auth is False:
                tm.showerror("Error", "Wrong Username or Password")#error Message
                              
  
        
    
class Logged(tk.Frame):
    #Logged In Page
    #Deletes logged info but still stored in
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        token = Logged.grabtoken()
        
        loggedtext = ttk.Label(self, text='Currently Logged in')
        loggedtext.grid(row=0, column=5, sticky=tk.E)

        label = ttk.Label(self, text="Stored Tools", font=("Verdana", 12))
        label.grid(row=0, column=0, sticky=tk.W)
        Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 9')

        maintext = ttk.Label(self, text="List of Registered Users: ", font=("Verdana", 11))
        emptytext = Label(self, width=20).grid(row=1, column=0)
        maintext.grid(row=2, column=0, sticky=tk.W)   
        subtext = ttk.Label(self, text=AllUsers(), wraplength=500, font='serif 10')
        subtext.grid(row=4, column=0, sticky=tk.W)
        
        
        
        def Temp():
            controller.show_frame(StartPage)
            Logged.deletetoken()

#######################################################        
        button1 = ttk.Button(self, text="Log Out",
                            command=lambda: Temp())#.get username and password from entry   
        button1.place(rely=0, relx=1.0, x=0, y=0, anchor=tk.NE)
#######################################################  
        button2 = ttk.Button(self, text="Register User",
                             command=lambda: controller.show_frame(RegisterPage))
        button2.place(rely=1.0, relx=0, x=0, y=0, anchor=tk.SW)
#######################################################  
        button3 = ttk.Button(self, text="Search Tool",
                            command=lambda: controller.show_frame(SearchToolPage))
        button3.place(rely=1.0, relx=0, x=86, y=0, anchor=tk.SW)
#######################################################
        button4 = ttk.Button(self, text="Invoice",
                            command=lambda: controller.show_frame(InvoicePage))
        button4.place(rely=1.0, relx=0, x=255, y=0, anchor=tk.SW)
####################################################### 
        button5 = ttk.Button(self, text="Create Tool",
                            command=lambda: controller.show_frame(RegisterToolPage))
        button5.place(rely=1.0, relx=0, x=170, y=0, anchor=tk.SW)
#######################################################       
        button6 = ttk.Button(self, text="Quit",
                            command=quit)
        button6.place(rely=1.0, relx=1.0, x=0, y=0, anchor=tk.SE)
#######################################################
        button7 = ttk.Button(self, text="Return Tool",
                            command=lambda: controller.show_frame(ReturnToolPage))
        button7.place(rely=1.0, relx=0, x=340, y=0, anchor=tk.SW)
####################################################### 

    def grabtoken():
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

    def deletetoken():
        filePath ='TempData/'
        for file in os.listdir(filePath):
            if file.endswith('.txt'):
                os.remove(filePath+file)            

class InvoicePage(tk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self,parent)
        label = ttk.Label(self, text="Stored Tools", font=("Verdana", 12))
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
                            command=lambda: backtologged())
        button1.place(rely=0, relx=1.0, x=0, y=0, anchor=tk.NE)
      
        button2 = ttk.Button(self, text="Quit",
                            command=quit)
        button2.place(rely=1.0, relx=1.0, x=0, y=0, anchor=tk.SE)

        emptybox = ttk.Label(self, text="")
        emptybox.grid(row=1, column=0)

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

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self,parent)
        label = ttk.Label(self, text="Stored Tools", font=("Verdana", 12))
        label.grid(row=0, column=0, sticky=tk.W)
        Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 9')

        def backtologged():
            try:
                f = open('TempData/login.txt')
                f.close()
                controller.show_frame(Logged)
            except FileNotFoundError:
                controller.show_frame(StartPage)
                
        emptytext = ttk.Label(self, text="")
        emptytext.grid(row=2,column=0)
        maintext = ttk.Label(self, text="Search Input:", font=("Verdana", 10))
        maintext.grid(row=3, column=0, sticky=tk.W)   
        search_entry = tk.Entry(self,width=40)
        search_entry.grid(row=4, column=0, sticky=tk.W)
        search_button = ttk.Button(self,text="Search",
                                  command= lambda: searchtool(search_entry.get()))
        search_button.grid(row=4, column=1, sticky=tk.W)
        emptytext = ttk.Label(self, text="")
        emptytext.grid(row=5,column=0)
        listbox = tk.Listbox(self,width=40)
        listbox.grid(row=6,column=0)

        
        def searchtool(x):
            listbox.delete(0, tk.END)
            x=x.lower()
            filePath = Tool.Path('tooldata')
            storedtools = []
            f = open(filePath + "ToolDir" + ".txt", "r")
            data = f.readlines()
            f.close()
            for line in data:
                if x in line:
                    listbox.insert(0, line.replace('\n', ''))
            
        def selectactive(x):
            tool_file = open(Tool.Path('tooldata') + str(x) + ".txt", "r")
            tool_data = tool_file.readlines()
            tool_file.close()
            if not os.path.exists('TempData/'):
                os.makedirs('TempData/')
            tempfile = 'TempData/activetool'
            output_file = open(tempfile + '.txt', 'w')
            output_file.writelines(tool_data)
            output_file.close()
            try:
                f = open('TempData/login.txt')
                user_id = f.readlines()
                f.close()
                myfile = open('TempData/activetool.txt', 'r')
                data = myfile.readlines()
                toolInfo = tk.Label(self,text='Tool Name: {0} | Tool Brand: {1}\n'.format(data[0].replace("\n", ""),
                                                                                          data[1].replace("\n", "")) +
                                    'Hire Cost: {0} | Tool Owner: {1}'.format(data[2].replace("\n", ""),
                                                                                          ownerInformation(data[3]).replace("\n", "")))

                temp = []
                for item in data:
                    if "2019 " in item:
                        temp.append(item.replace(" \n", ""))#not future proofed
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
                            
                
        
                
            except FileNotFoundError:
                tm.showerror("Error", "Please login to access this page.")
                controller.show_frame(StartPage)
    
            
        def ownerInformation(user_id):
            f = open('UserData/'+ user_id.replace("\n", "") + '.txt')
            data = f.readlines()
            return data[1]

            
        moreinfo_search = ttk.Button(self, text="More Information",
                                     command= lambda: selectactive(listbox.get(tk.ACTIVE)))
        moreinfo_search.grid(row=6, column=1)
        
        
        button1 = ttk.Button(self, text="Back to Main",
                            command=lambda: backtologged())
        button1.place(rely=0, relx=1.0, x=0, y=0, anchor=tk.NE)
      
        button2 = ttk.Button(self, text="Quit",
                            command=quit)
        button2.place(rely=1.0, relx=1.0, x=0, y=0, anchor=tk.SE)


  


        
class RegisterToolPage(tk.Frame):
    #Logged In Page
    #Deletes logged info but still stored in
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Logged In", font=LARGE_FONT)
        label.place
        label = ttk.Label(self, text="Stored Tools", font=("Verdana", 12))
        label.grid(row=0, column=0, sticky=tk.W)
        Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 9')

        def backtologged():
            try:
                f = open('TempData/login.txt')
                f.close()
                controller.show_frame(Logged)
            except FileNotFoundError:
                controller.show_frame(StartPage)
        
####################################################### 
        button1 = ttk.Button(self, text="Back to Main",
                            command=lambda:backtologged())
        button1.place(rely=0, relx=1.0, x=0, y=0, anchor=tk.NE)
#######################################################       
        button6 = ttk.Button(self, text="Quit",
                            command=quit)
        button6.place(rely=1.0, relx=1.0, x=0, y=0, anchor=tk.SE)
#######################################################
        
        maintext = ttk.Label(self, text="Tool Registration Form: ", font=("Verdana", 11))
        emptytext = Label(self, width=20).grid(row=1, column=0)
        maintext.grid(row=2, column=0, sticky=tk.W)

        
        toolname = ttk.Label(self, text="Tool Name")
        toolname.grid(row=4, column=0, sticky=tk.W)
        toolname_i = ttk.Entry(self)
        toolname_i.grid(row=5, column=0, sticky=tk.W)

        toolbrand = ttk.Label(self, text="Tool Brand")
        toolbrand.grid(row=6, column=0, sticky=tk.W)
        toolbrand_i = tk.Entry(self)
        toolbrand_i.grid(row=7, column=0, sticky=tk.W)

        dayrate = ttk.Label(self, text="Day Rate")
        dayrate.grid(row=8, column=0, sticky=tk.W)
        dayrate_i = tk.Entry(self)
        dayrate_i.grid(row=9, column=0, sticky=tk.W)

        start = ttk.Label(self, text="Start Date")
        start.grid(row=4, column=1, sticky=tk.W)
        start_i = tk.Entry(self)
        start_i.grid(row=5, column=1, sticky=tk.W)
        warning_start = ttk.Label(self, text="Input format as DD-MM-YYYY")
        warning_start.grid(row=5,column=2, sticky=tk.W)
        #DD-MM-YYYY
        end = ttk.Label(self, text="End Date")
        end.grid(row=6, column=1, sticky=tk.W)
        end_i = tk.Entry(self)
        end_i.grid(row=7, column=1, sticky=tk.W)
        warning_end = ttk.Label(self, text="Input format as DD-MM-YYYY")
        warning_end.grid(row=7,column=2, sticky=tk.W)

        submit = ttk.Button(self, text="Submit",
                            command=lambda: createNewTool(toolname_i.get(), toolbrand_i.get(),
                                                          dayrate_i.get(), start_i.get(),
                                                          end_i.get()))#.get username and password from entry   
        submit.grid(row=8, column=1, sticky=tk.W)
        def createNewTool(toolname, toolbrand, dayrate, start, end):
            start = datetime.datetime.strptime(start, "%d-%m-%Y") 
            end = datetime.datetime.strptime(end, "%d-%m-%Y")
            trueEnd = (end-start).days + 1
            token = grabtemp('login', 0)
            date_generated = [start + datetime.timedelta(days=x) for x in range(0, trueEnd)]
            dList = []
            for x in date_generated:
                dList.append(x.strftime("%d-%m-%Y"))
            nList = (' \n'.join(dList))
            tool = Tool.createTool(toolname.lower(), toolbrand.lower(),token,dayrate,nList)
            #print('New tool with the owner: ' + str(token) + ' is created.')
            filePath = User.Path('userdata')
            for file in os.listdir(filePath):
                if file.startswith(str(token)):
                    with open(filePath+file, 'a') as myfile:
                        myfile.write(str(tool+"\n"))
            f = open("ToolData/ToolDir.txt", "a+")
            f.write(toolname + "\n")
            f.close
            

            
class RegisterPage(tk.Frame): #Logged In Page

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Logged In", font=LARGE_FONT)
        label.place
        label = ttk.Label(self, text="Stored Tools ", font=("Verdana", 12))
        label.grid(row=0, column=0, sticky=tk.W)
        Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 9')

        def backtologged():
            try:
                f = open('TempData/login.txt')
                f.close()
                controller.show_frame(Logged)
            except FileNotFoundError:
                controller.show_frame(StartPage)
        
####################################################### 
        button1 = ttk.Button(self, text="Back to Main",
                            command=lambda:backtologged())
        button1.place(rely=0, relx=1.0, x=0, y=0, anchor=tk.NE)
#######################################################       
        button6 = ttk.Button(self, text="Quit",
                            command=quit)
        button6.place(rely=1.0, relx=1.0, x=0, y=0, anchor=tk.SE)
#######################################################
        
        maintext = ttk.Label(self, text="Registration Form: ", font=("Verdana", 11))
        emptytext = Label(self, width=20).grid(row=1, column=0)
        maintext.grid(row=2, column=0, sticky=tk.W)

        
        forename = ttk.Label(self, text="Forename")
        forename.grid(row=4, column=0, sticky=tk.W)
        forename_i = ttk.Entry(self)
        forename_i.grid(row=5, column=0, sticky=tk.W)

        surname = ttk.Label(self, text="Surname")
        surname.grid(row=6, column=0, sticky=tk.W)
        surname_i = tk.Entry(self)
        surname_i.grid(row=7, column=0, sticky=tk.W)

        address = ttk.Label(self, text="Post Code")
        address.grid(row=8, column=0, sticky=tk.W)
        address_i = tk.Entry(self)
        address_i.grid(row=9, column=0, sticky=tk.W)

        email = ttk.Label(self, text="Email")
        email.grid(row=4, column=1, sticky=tk.W)
        email_i = ttk.Entry(self)
        email_i.grid(row=5, column=1, sticky=tk.W)

        password = ttk.Label(self, text="Password")
        password.grid(row=6, column=1, sticky=tk.W)
        password_i = ttk.Entry(self)
        password_i.grid(row=7, column=1, sticky=tk.W)

        submit = ttk.Button(self, text="Submit",
                            command=lambda: createNewUser(forename_i.get(), surname_i.get(),
                                                          address_i.get(), email_i.get(),
                                                          password_i.get()))#.get username and password from entry   
        submit.grid(row=9, column=1, sticky=tk.W)
        
        def createNewUser(userForename, userSurname, userAddress, userEmail, userPassword): #Creates account with User class.
            counter = 0
            listoflist = [userForename, userSurname, userAddress, userEmail, userPassword]
            val = 0
            while counter < 5:
                if listoflist[counter] == '':
                    pass
                else:
                    val = val + 1
                
                counter = counter + 1

            if val == 5:
                user = User.createUser(userForename, userSurname, userAddress,userEmail,userPassword) #Classes/User
                controller.show_frame(StartPage)
                tm.showinfo("Registered", "You can now Login.")
            else:
                tm.showerror("Error", "Parameter(s) not entered.")

        
class ReturnToolPage(tk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

Logged.deletetoken()

def __main__():
    app = SharedTool()#app run
    app.geometry("620x300")
    app.resizable(0, 0)
    app.mainloop()#loop

__main__()
