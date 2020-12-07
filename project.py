#This program is a bracket maker. A user can import a text file with a list of teams and the program
#will automatically create matchings.
#One can also randomize the teams and determine how many weeks there will be.

#USAGE: IN THE TEXT FILE, HAVE ONE TEAM PER LINE.

from tkinter import Tk, Label, Button, filedialog, Toplevel, Listbox, Entry, ttk, IntVar, Checkbutton, END, PhotoImage
import random


# This creates the gui and all its functionality in terms of what can be pressed
class BracketGUI:

    #Main page, what can be seen when first opened
    def __init__(self, master):
        self.master = master
        master.title("Bracket Master!")
        master.geometry("500x600")
        master.configure(bg="skyblue")
        self.label = Label(master, text="This program is used to make a bracket for teams to fight each other!",
                           height=10, width=55, bg="skyblue")
        self.label.pack()

        self.iport_button = Button(master, text="Click here to import file of team names", command=self.iport, height=4,
                                   width=30, bg="pink")
        self.iport_button.pack()

        self.type_button = Button(master, text="Click here to type in team names", command=self.type, height=4,
                                  width=30, bg="pink")
        self.type_button.pack()

        #COMMENT THIS OUT IF YOU DO NOT HAVE THE IMAGE FILE
        #self.photo = PhotoImage(file="BM.png")
        #self.imglabel = Label(master, image=self.photo, height=300, width=300)
        #self.imglabel.pack()
        ##

    def saveDoc(self, matchList): #This opens the save file dialog, allows user to save the list of matches
        file = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if file is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        for i in range(len(matchList)):
            
            file.write("\n\n\nWeek "+str(i+1)+"\n")            
            for matchitem in matchList[i].get(0, END):  #Looks through each tab in the window and writes what is written there              
                file.write(matchitem+"\n") 
        file.close()
        

    #This is for the secondary window; displays the matchings.
    def updateFields(self, weeks):

        
        if self.newWin.counter:#This destroys any previous widgits if the user wants to change the number of weeks there are
            self.newWin.tabs.destroy()
            self.newWin.title1.destroy()
            self.newWin.savefile.destroy()
        if self.newWin.randomize.get() == 1:#This randomizes the fields if the user has the box checked
            random.shuffle(self.listings)
        self.newWin.title1 = Label(self.newWin, text="Here are your matchings")
        self.newWin.title1.pack()
        self.newWin.tabs = ttk.Notebook(self.newWin) #The tabs for each week
        weekTab = []
        for i in range(weeks): #Creates a list, each item being one tab
            weekTab.append(ttk.Frame(self.newWin.tabs))
            self.newWin.tabs.add(weekTab[i], text='Week ' + str(i + 1))
        self.newWin.tabs.pack(fill='both', expand=1)
        matchList = []
        for i in weekTab: #Creates the textbox in each tab in which it will contain the matchings
            matchList.append(Listbox(i))

        for i in range(len(self.listings)): #Systematically sorts the matchings into the text-boxes
            matchList[i % weeks].insert(i + 1, self.listings[i][0] + " vs " + self.listings[i][1])
        for i in range(weeks):
            matchList[i].pack(fill='both', expand=1)
        self.newWin.savefile = Button(self.newWin, text="Save", command=lambda: self.saveDoc(matchList), height=4,
                                  width=30, bg="pink") #Save the matchings button
        self.newWin.savefile.pack()

        self.newWin.counter = True #To indicate that the user has clicked update (for any future updates, the program will delete and recreate the tabs



        
    def validateNum(self, inputnum): #Ensure the number of weeks is an integer
        try:
            weeksNum = int(inputnum)
            self.updateFields(weeksNum)
        except ValueError:
            print("Not a num")

    def newWindow(self): #Creates the new window in which the team matchings will appear
        self.newWin = Toplevel()
        self.newWin.geometry("500x500")
        self.newWin.counter = False #When the program is first created, no matchings are shown, so any attempts to update should occur
        self.newWin.wm_title("Team matchings")
        self.newWin.weeksinfo = Label(self.newWin, text="Input the number the amount of weeks there are")
        self.newWin.weeksinfo.pack()
        self.newWin.weeks = Entry(self.newWin)
        self.newWin.weeks.pack()
        self.newWin.randomize = IntVar() #This assigns the checkbox variable to an object variable
        self.newWin.chk = Checkbutton(self.newWin, text="Randomize?", variable=self.newWin.randomize)#Checkbox for randomize or not
        self.newWin.chk.pack()
        self.newWin.updateButton = Button(self.newWin, text="Update",
                                          command=lambda: self.validateNum(self.newWin.weeks.get())) #Is called when the user clicks update
        self.newWin.updateButton.pack()

    def enterbutton(self): #This function takes the team entered and appends it to a list of all team names
        Teamname=self.entryWin.weeks.get()
        self.entryWin.weeks.delete(0,'end')
        if Teamname !="":
            self.teamlist.append(Teamname)
        else: #If nothing is entered
            print("Please type a team name!")

    def finishbutton(self): #Sorts the list and creates the matchings in a new list
        if len(self.teamlist)>=2:
            self.listings = self.sortfunc(self.teamlist)
            self.entryWin.destroy()
            self.newWindow()
        else:
            print ("Please enter at least 2 team names.") #You can't only have one team
        
    def entryWindow(self): #Window for the manual entry 
        self.teamlist=[]
        self.entryWin = Toplevel()
        self.entryWin.geometry("500x500")
        
        self.entryWin.wm_title("Team Name Entry")
        self.entryWin.weeksinfo = Label(self.entryWin, text="Input team names, you MUST click 'enter' after each name you input!")
        self.entryWin.weeksinfo.pack()
        self.entryWin.weeks = Entry(self.entryWin)
        self.entryWin.weeks.pack()
        self.entryWin.EnterButton = Button(self.entryWin, text="Enter",
                                          command=self.enterbutton)
        self.entryWin.EnterButton.pack()
        self.entryWin.FinishButton = Button(self.entryWin, text="Finish",
                                          command=self.finishbutton)
        self.entryWin.FinishButton.pack()
    
    
       
##    def sortfunc(self, list1): #The algorithmn that creates the listings; systematically goes through all the possible combinations
##        sorted_list = []
##        for name1 in list1[:-1]:
##            for name2 in list1[list1.index(name1) + 1:]:
##                sorted_list.append([name1, name2])
##        random.shuffle(sorted_list)
##        return sorted_list

    def sortfunc(self, list1): #The algorithm that creates the listings; systematically goes through all the possible combinations
        sorted_list = []
        for name1 in range(len(list1)-1):
            for name2 in range(name1+1, len(list1)):
                sorted_list.append([list1[name1], list1[name2]])
        random.shuffle(sorted_list)
        return sorted_list


    def iport(self): #Import a text file with team names
        self.teamlist = open(filedialog.askopenfilename(initialdir="/", title="Select file",
                                                        filetypes=(("Text file", "*.txt"), ("all files", "*.*"))),
                             "r").readlines()
        for i in range(len(self.teamlist)):
            self.teamlist[i] = self.teamlist[i].replace('\n', '')
            self.teamlist[i] = self.teamlist[i].strip() #Creates a list of the team names, strips whitespace
        self.listings = self.sortfunc(self.teamlist)
        self.newWindow()



    def type(self): #Calls the new window for manual entry
        self.entryWindow()



root = Tk()
gui1 = BracketGUI(root)

root.mainloop()
