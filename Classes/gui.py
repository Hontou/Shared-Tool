import tkinter as tk
import tkinter.messagebox as tm
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
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Stored Tools Login Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        #####Login Inputs#####
        username = tk.Label(self, text="Email")
        username.pack(side=tk.LEFT)
        username_i = tk.Entry(self)
        username_i.pack(side=tk.LEFT)
        password = tk.Label(self, text="Password")
        password_i = tk.Entry(self)
        password.pack(side=tk.LEFT)
        password_i.pack(side=tk.LEFT)
        #####Login Inputs#####

        
        button1 = tk.Button(self, text="Log In",
                            command=lambda: logcheck(username_i.get(), password_i.get()))#.get username and password from entry
        
        button1.pack()

        button2 = tk.Button(self, text="Register",
                            command= createNewUser)
        button2.pack()

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
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Logged In", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back to Main",
                            command=lambda:controller.show_frame(StartPage))
        button1.pack()


##############################################################################################

def createNewUser(): #Creates account with User class.
    userForename = input('> Forename: ')
    userSurname = input('> Surname: ')
    userAddress = input('> Address: ')
    userEmail = input('> Email: ')
    userPassword = input('> Password: ')
    user = User.createUser(userForename, userSurname, userAddress,userEmail,userPassword) #Classes/User
    print('New user with id: ' + user + ' created.') #unique id generated





app = SharedTool()#app run
app.mainloop()#loop

