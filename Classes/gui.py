import tkinter as tk
import tkinter.messagebox as tm
from tkinter import ttk
from tkinter.ttk import Frame, Label, Style
from User import *
from Tool import *
from Time import *
import datetime

LARGE_FONT=("Verdana", 12) #standard font



##############################################################################################

class SharedTool(tk.Tk): #Initializer

    def __init__(self): #Constructors
        tk.Tk.__init__(self)
 
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand= True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

    
        
        self.frames = {}

        for F in (StartPage, PageOne):
            
            frame = F(container, self)
            
            self.frames[F] = frame
            frame.grid(row=0, column = 0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame): #Start Page

    def __init__(self, parent, controller):
        global username_i
        global password_i
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
        button1 = ttk.Button(self, text="Log In",
                            command=lambda: logcheck(username_i.get(), password_i.get()))#.get username and password from entry   
        button1.grid(row=0,column=6, sticky=tk.E)
#######################################################  
        button2 = ttk.Button(self, text="Quit",
                            command= createNewUser)
        button2.place(rely=1.0, relx=1.0, x=0, y=0, anchor=tk.SE)
#######################################################  
        button3 = ttk.Button(self, text="Create Tool",
                            command= createNewUser)
        button3.place(rely=1.0, relx=0, x=255, y=0, anchor=tk.SW)
#######################################################  
        button4 = ttk.Button(self, text="Hire Tool",
                            command= createNewUser)
        button4.place(rely=1.0, relx=0, x=170, y=0, anchor=tk.SW)
#######################################################  
        button5 = ttk.Button(self, text="Search Tool",
                            command= createNewUser)
        button5.place(rely=1.0, relx=0, x=86, y=0, anchor=tk.SW)
#######################################################  
        button6 = ttk.Button(self, text="Register User",
                             command=quit)
        button6.place(rely=1.0, relx=0, x=0, y=0, anchor=tk.SW)
#######################################################
        
        def logcheck(email, password):  #New Login taken from __main__. Displays if username or password wrong with a FOR/IF statement.
            auth = None
            filePath = User.Path('userdata')
            for file in os.listdir(filePath):
                if file.endswith(".txt"):
                    with open(filePath+file,'r') as myfile:
                        data = myfile.readlines()
                        if email == str(data[3].strip('\n')):
                            if password == str(data[4].strip('\n')):
                                print('Logged in as '+data[1])
                                controller.show_frame(PageOne)
                                auth = True
                                return data[1]
                            else:
                                auth = False
                        else:
                            auth = False
                                
            if auth is False:
                tm.showerror("Error", "Wrong Username or Password")#error Message
                                    
        
        
    
class PageOne(tk.Frame): #Logged In Page

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Logged In", font=LARGE_FONT)
        label.grid(row=0, column=0)
        button1 = ttk.Button(self, text="Back to Main",
                            command=lambda:controller.show_frame(StartPage))
        button1.grid(row=0, column=0)


##############################################################################################

def createNewUser(): #Creates account with User class.
    userForename = input('> Forename: ')
    userSurname = input('> Surname: ')
    userAddress = input('> Address: ')
    userEmail = input('> Email: ')
    userPassword = input('> Password: ')
    user = User.createUser(userForename, userSurname, userAddress,userEmail,userPassword) #Classes/User
    print('New user with id: ' + user + ' created.') #unique id generated


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
                        
            return '\n'.join(stored[:30])

app = SharedTool()#app run
app.geometry("620x300")
app.resizable(0, 0)
app.mainloop()#loop

