"""
Script for matching database information to user files
Date: 08/09/2017
"""
import os
from tkinter import *
from tkinter import messagebox

"""
method which reads in the database from file and returns a dictionary, number
of columns in the database and  approperiate headings tanken from the database
"""
def getDB(db):
    START = 4  # colum the data is added from ( onwards)
    dbLoc = os.getcwd() + "\\databases\\" #db location
    repeats = 0 #used to warn the user of non-identical probes

    try :
        database = open(dbLoc + db, "r")
        db =  {}
        dbCols = 0 #number of columns in the file
        header = ""
        dblines = database.readlines()

    except:
        tError = "Database Error"
        sError = "Unable to open the database file. Please check your file."
        messagebox.showwarning(tError,sError)
        return ""

    for i in range(len(dblines)):
        if i == 0:
            temp = dblines[i].split("\t")
            dbCols = len(temp) #

            if dbCols <= START:
                tError = "Database Error"
                sError = "Your Database does not have enough columns. Please refer to documentation"
                messagebox.showwarning(tError,sError)
                return ""

            j = START
            while j < dbCols:
                header = header  + temp[j] + "\t"
                j = j + 1

        else:
            temp = dblines[i].split("\t")

            for j in range(len(temp)):
                temp[j] = temp[j].strip()

            if temp[0] in db:
                repeats = repeats + 1
            else:
                dbInfo = []
                k = START
                while k < dbCols:
                    dbInfo.append(temp[k])
                    k = k +1

            db.update({temp[0] : dbInfo}) #get probe and column

    if repeats > 0:
        sError = "Not all of your probes were unique - there were " + str(repeats) + " duplicate probes. Please refer to the documentation"
        messagebox.showwarning("Please note",sError)

    return [db, dbCols, header]

def matchFile(fileInput, database, fileOutput):

    ############## Read Databases #################
    returns = getDB(database) #returns a list

    if returns != "":
        db = returns[0]
        size = returns[1]
        header = returns[2]
            #########Process Outout File#################
        outputLoc = os.getcwd() + "\\output\\"
        #open file
        try:
            fileIn = open(fileInput, "r")
            fileLines = fileIn.readlines()
        except:
            tError = "File Error"
            sError = "It was not able to open the selected file, please try again"
            messagebox.showwarning(tError,sError)

        ######find dimensions of the user Input File###############
        firstProbe  = 0 #line where probe data is found
        foldChange = 0
        lastRow = len(fileLines) -1 #number of items in the file  (starts at 1)
        lastCol= 0
        prim = 0
        entrez = 0

        dataStart  = fileLines[firstProbe]

        while dataStart[:2] != "A_" and firstProbe <= lastRow:
            firstProbe = firstProbe + 1
            dataStart = fileLines[firstProbe]


        if dataStart[:2] == "A_":
            if firstProbe == 0:
                tError = "File Error"
                sError = "There were no column titles  - please check documentation and try again"
                messagebox.showwarning(tError,sError)
            else:
                try:
                    w = open(outputLoc+fileOutput, "w")  #new file
                except:
                    tError = "System Error"
                    sError = "File Destination not found - please refer to documentation"
                    messagebox.showwarning(tError,sError)

                if firstProbe-2 > 0:
                    titleEx = fileLines[firstProbe-2]
                    w.write(titleEx)

                titleData = fileLines[firstProbe-1].split("\t")
                for element in range(len(titleData)):
                    titleData[element] = titleData[element].strip()

                lastCol = len(titleData) - 1

                ###find approperiate columns in the user file
                for item in range(len(titleData)):
                    if titleData[item] == "foldchange":
                        foldChange = item
                    if titleData[item] == "EntrezGeneID":
                        entrez = item
                    if titleData[item] == "PrimaryAccession":
                        prim = item

                if foldChange == 0:

                    tError = "File Errors"
                    sError = "foldchange was not included in the file, please try again"
                    messagebox.showwarning(tError,sError)
                elif entrez == 0:
                        tError = "File Errors"
                        sError = "EntrezGeneID was not included in the file, please try again"
                        messagebox.showwarning(tError,sError)
                elif prim ==0:
                    tError = "File Errors"
                    sError = "PrimaryAccession was not included in the file, please try again"
                    messagebox.showwarning(tError,sError)
                else:
                    title =""
                    count = 0

                    while count <= foldChange:
                        title= title + titleData[count] + "\t"
                        count = count+1

                    title = title +  titleData[entrez] +"\t"+ titleData[prim] + "\t" +  header + "\n"

                    w.write(title)

                    #write to file
                    for i in range(firstProbe,lastRow):
                        writer = ""
                        line = fileLines[i].split("\t")
                        for element in range(len(line)):
                            line[element] = line[element].strip()

                        for j in range(0,foldChange+1):
                            writer = writer + line[j] + "\t"

                        a = db.get(line[0], "notfound")

                        dbInfo = ""
                        result =  db.get(line[0], "notfound")
                        if result == "notfound":
                            dbInfo = result
                        else:
                            for i in range(len(result)):
                                dbInfo = dbInfo + result[i] + "\t"
                        writer = writer + line[entrez] + "\t" + line[prim] + "\t" + dbInfo+  "\n"
                        w.write(writer)
        else:
            tError = "File Error"
            sError = "No probes were found in the database"
            messagebox.showwarning(tError,sError)
