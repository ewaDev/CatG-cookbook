"""
Grahical User Interface for CatG - a mircoarray matching tool
Author: Ewa G
Date: 08/09/2017
"""

from dataProcess import matchFile
from tkinter import *
from tkinter import messagebox
import os


class UserInterface():

    """
    method checks for a presence of an already existing file, prevents
    files from being mistakenly overriten.  It  asks the user whether they want
    to overwrite the files
    """
    def filePresenceCheck(self, filename):
        files = os.listdir(os.getcwd() + "\\output\\")
        try:
            files.index(filename)
            tError = "User Input Error"
            sError = "The output file with the name " + "\" " + filename[:len(filename)-4] + "\" " + " already exists as the output file. Would you like to override the existing file?"
            answer = messagebox.askyesno(tError, sError)
            return answer
        except:
            return True


    #launch the file browser and locate the file which the user wants to process
    def browsecsv(self,event):
        from tkinter import filedialog
        filename = filedialog.askopenfilename(initialdir = "C:/",title = "choose your file",filetypes = (("txt files","*.txt"),("all files","*.*"))) #pnly shows .txt files
        if filename !="":
            if filename[-3:].lower() == "txt":
                position = filename.rfind('/')
                self.browseButton.configure(text = filename[position+1:]) #update the button label to represent that the file was read in
                self.strFileLocation.set(filename)
            else:
                tError = "File Error"
                sError = "You have provided a file which is not a txt. Unfortunately CATG only supports .txt files."
                messagebox.showwarning(tError,sError)
        return "break" #removes button press

    #method for collecting all of the user provided information and processing them
    def getInput(self,event):
        fileInput = self.strFileLocation.get()
        fileOutput = self.nameEntry.get().strip()
        dbstr = "".join(map(str, self.listbox.curselection()))

        sError = ""
        if fileInput =="":
            tError = "User Input Error"
            sError = "You didn't select a file to process"
            return "break"
            messagebox.showwarning(tError,sError)
        elif dbstr == "":
            tError = "User Input Error"
            sError = "You didn't select a database to use"
            messagebox.showwarning(tError,sError)
            return "break"
        elif fileOutput == "":
            tError = "User Input Error"
            sError = "You didn't provide a name for your output file"
            messagebox.showwarning(tError,sError)
            return "break"
        else:
            fileOutput = fileOutput + ".txt"
            check = self.filePresenceCheck(fileOutput)

            if check == True:
                try:
                    self.goButton.configure(text = "processing your file...") #updates the button label
                    database = self.names[int(dbstr)]
                    matchFile(fileInput, database, fileOutput)
                    messagebox.showinfo("Please Note","Your file was processed!")
                    self.goButton.configure(text = "Process File")
                    return "break" #removes button press
                except:
                    self.goButton.configure(text = "Process File")
                    tError = "System Error"
                    sError = "Your file was not processed"
                    messagebox.showwarning("Error",sError)
            else:
                return "break"



    #method for returning all of the database names in the databases folder
    def getLocation(self):
        files = os.listdir(os.getcwd() + "\\databases")
        dblist = []
        for f in range(len(files)):
            if files[f][:2] == "Db":
                dblist.append(files[f])
        return dblist

    #Initialise the GUI window
    def __init__(self, root, *args, **kwargs):
        self.root = root

        #color scheme
        lightC = "#C5C1C0"
        blackC = "#0A1612"
        denimC = "#1A2930"
        goldC = "#F7CE3E"

        root.title("CatG")
        root.configure(background=denimC)
        self.strFileLocation =StringVar()
        strFileOutput =StringVar()

        frame = Frame(root)
        title = Label(root, text= "Welcome to CATG",font=("Georgia", 18, "bold"),fg=goldC, bg = denimC).grid(sticky=W, padx=100,columnspan=3)
        Label(root, bg = denimC).grid(row = 1)
        BrowseLabel = Label(root, text= "Select a File: ", fg=lightC, bg = denimC, font=("Verdana",12)).grid(sticky=W+E,row=2,column=0,padx = 10 )
        self.browseButton = Button(root, text = "Browse...", font=("Verdana",10), bg=lightC)
        self.browseButton.bind("<Button-1>",self.browsecsv)
        self.browseButton.grid(sticky=W+E,row=2, column=1)

        nameLabel = Label(root, text= "Name your output: ", fg=lightC, bg = denimC, font=("Verdana",12)).grid(sticky=W+E,row=3,column=0, columnspan = 1, padx = 10)
        self.nameEntry = Entry(root, textvariable=strFileOutput)
        self.nameEntry.grid(sticky=W+E,row=3, column=1)

        dbLabel = Label(root, text ="Pick your database", fg=lightC, bg = denimC, font=("Verdana",12)).grid(sticky=W+E,row =4, column = 0,padx = 10)
        self.listbox = Listbox(root,selectmode=SINGLE)
        self.names = self.getLocation()

        #add all the files in the folder to the listbox
        for i in range(len(self.names)):
            self.listbox.insert(END,self.names[i])

        self.listbox.grid(sticky=W+E,row =4, column = 1)

        self.goButton = Button(root, text = "Process File", height = 1, width = 40, bg=lightC)
        self.goButton.grid(row=6, columnspan = 3, pady = 10)
        self.goButton.bind("<Button-1>",self.getInput)

#Program Start
if __name__ == '__main__':
    root = Tk()
    UserInterface(root)
    root.mainloop() #keeps the gui running and responsive
