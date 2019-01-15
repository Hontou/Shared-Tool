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


##############################################################################################

class SharedTool(tk.Tk): #Initializer

    def __init__(self): #Constructors
        tk.Tk.__init__(self)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand= True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

    
        
        self.frames = {}

        for F in (StartPage, Logged, RegisterPage, RegisterToolPage):
            
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
        label = ttk.Label(self, text="Stored Tools Login Page", font=("Verdana", 12))
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
                            command= False)
        button3.place(rely=1.0, relx=0, x=86, y=0, anchor=tk.SW)
#######################################################  
        button4 = ttk.Button(self, text="Hire Tool",
                            command= False)
        button4.place(rely=1.0, relx=0, x=170, y=0, anchor=tk.SW)
#######################################################  
        button5 = ttk.Button(self, text="Create Tool",
                            command=lambda: failedlogin())
        button5.place(rely=1.0, relx=0, x=255, y=0, anchor=tk.SW)
#######################################################       
        button6 = ttk.Button(self, text="Quit",
                            command=quit)
        button6.place(rely=1.0, relx=1.0, x=0, y=0, anchor=tk.SE)
#######################################################   
        def failedlogin():
            tm.showerror("Error", "Please login/register an account before creating.")
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
                                tempfile = 'TempData/'+str(x)
                                output_file = open(tempfile + '.txt', 'w')
                                output_file.write(data[0]+data[1]+data[2]+data[3]+data[4])
                                output_file.close()
                                return data[1]
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

        label = ttk.Label(self, text="Stored Tools Login Page", font=("Verdana", 12))
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
                            command= False)
        button3.place(rely=1.0, relx=0, x=86, y=0, anchor=tk.SW)
#######################################################  
        button4 = ttk.Button(self, text="Hire Tool",
                            command= False)
        button4.place(rely=1.0, relx=0, x=170, y=0, anchor=tk.SW)
#######################################################  
        button5 = ttk.Button(self, text="Create Tool",
                            command=lambda: controller.show_frame(RegisterToolPage))
        button5.place(rely=1.0, relx=0, x=255, y=0, anchor=tk.SW)
#######################################################       
        button6 = ttk.Button(self, text="Quit",
                            command=quit)
        button6.place(rely=1.0, relx=1.0, x=0, y=0, anchor=tk.SE)
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
            
class RegisterToolPage(tk.Frame):
    #Logged In Page
    #Deletes logged info but still stored in
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Logged In", font=LARGE_FONT)
        label.place
        label = ttk.Label(self, text="Stored Tools Login Page", font=("Verdana", 12))
        label.grid(row=0, column=0, sticky=tk.W)
        Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 9')
        
####################################################### 
        button1 = ttk.Button(self, text="Back to Main",
                            command=lambda:controller.show_frame(StartPage))
        button1.place(rely=0, relx=1.0, x=0, y=0, anchor=tk.NE)
#######################################################  
        button2 = ttk.Button(self, text="Register User",
                             command=lambda: controller.show_frame(RegisterPage))
        button2.place(rely=1.0, relx=0, x=0, y=0, anchor=tk.SW)
#######################################################  
        button3 = ttk.Button(self, text="Search Tool",
                            command= False)
        button3.place(rely=1.0, relx=0, x=86, y=0, anchor=tk.SW)
#######################################################  
        button4 = ttk.Button(self, text="Hire Tool",
                            command= False)
        button4.place(rely=1.0, relx=0, x=170, y=0, anchor=tk.SW)
#######################################################  
        button5 = ttk.Button(self, text="Create Tool",
                            command= False)
        button5.place(rely=1.0, relx=0, x=255, y=0, anchor=tk.SW)
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
############################################################        
############################################################
############################################################
        start = ttk.Label(self, text="Start Date")
        start.grid(row=4, column=1, sticky=tk.W)
        start_i = tk.Button(self, text="Pick a Date", command=lambda: application())
        start_i.grid(row=5, column=2, sticky=tk.W)

        end = ttk.Label(self, text="End Date")
        end.grid(row=6, column=1, sticky=tk.W)
        end_i = tk.Button(self, text="Pick a Date", command=lambda: application())
        end_i.grid(row=7, column=2, sticky=tk.W)
        

############################################################        
############################################################
############################################################
        submit = ttk.Button(self, text="Submit")
        submit.grid(row=9, column=1, sticky=tk.W)
        def createNewTool(token, toolName, toolBrand, DayRate):
            toolName = input('> Name: ')
            toolBrand = input('> Brand: ')
            DayRate = input('> Day Rate: ')
            bookD = hireTime()
            tool = Tool.createTool(toolName, toolBrand,token,DayRate,bookD)
            print('New tool with the owner: ' + str(token) + ' is created.')
            filePath = User.Path('userdata')
            for file in os.listdir(filePath):
                if file.startswith(str(token)):
                    with open(filePath+file, 'a') as myfile:
                        myfile.write(str(tool+"\n"))
            f = open("ToolData/ToolDir.txt", "a+")
            f.write(toolName + "\n")
            f.close
        def hireTime():
            start = datetime.datetime.strptime(start, "%d-%m-%Y") 
            end = datetime.datetime.strptime(end, "%d-%m-%Y")
            trueEnd = (end-start).days + 1
            date_generated = [start + datetime.timedelta(days=x) for x in range(0, trueEnd)]
            dList = []
            for x in date_generated:
                dList.append(x.strftime("%d-%m-%Y"))
            return(' \n'.join(dList))

            
class RegisterPage(tk.Frame): #Logged In Page

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Logged In", font=LARGE_FONT)
        label.place
        label = ttk.Label(self, text="Stored Tools Login Page", font=("Verdana", 12))
        label.grid(row=0, column=0, sticky=tk.W)
        Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 9')
        
####################################################### 
        button1 = ttk.Button(self, text="Back to Main",
                            command=lambda:controller.show_frame(StartPage))
        button1.place(rely=0, relx=1.0, x=0, y=0, anchor=tk.NE)
#######################################################  
        button2 = ttk.Button(self, text="Register User",
                             command=lambda: controller.show_frame(RegisterPage))
        button2.place(rely=1.0, relx=0, x=0, y=0, anchor=tk.SW)
#######################################################  
        button3 = ttk.Button(self, text="Search Tool",
                            command= False)
        button3.place(rely=1.0, relx=0, x=86, y=0, anchor=tk.SW)
#######################################################  
        button4 = ttk.Button(self, text="Hire Tool",
                            command= False)
        button4.place(rely=1.0, relx=0, x=170, y=0, anchor=tk.SW)
#######################################################  
        button5 = ttk.Button(self, text="Create Tool",
                            command= False)
        button5.place(rely=1.0, relx=0, x=255, y=0, anchor=tk.SW)
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
                print('New user with id: ' + user + ' created.') #unique id generated
            else:
                tm.showerror("Error", "Parameter(s) not entered.")

        
##############################################################################################

Logged.deletetoken()

def __main__():
    app = SharedTool()#app run
    app.geometry("620x300")
    app.resizable(0, 0)
    app.mainloop()#loop

__main__()
