"""
Script for retrieval of data from KEGG database via using
the KEGG website
Date: 08/09/2017
"""

from selenium import webdriver
import datetime
import sys
import time

"""
Method for returning the approperiate url
based on the oeirmary accession number.
"""

def returnUrl(geneName):
    ###organisms found via http://www.kegg.jp/kegg-bin/get_htext?htext=br08601.keg&query=cft073

    if geneName[:1] == "b":
        #Escherichia coli K-12 MG1655
        url = "http://www.genome.jp/dbget-bin/www_bget?" + "eco:" + geneName
        return url
    elif geneName[:1] == "c":
        #Escherichia coli O6:K2:H1 CFT073
        geneName = geneName.replace("_", "")
        url = "http://www.genome.jp/dbget-bin/www_bget?" + "ecc:" + geneName
        return url
    elif geneName[:1] == "E":
        #Escherichia coli O157:H7 Sakai
        url = "http://www.genome.jp/dbget-bin/www_bget?" + "ecs:" + geneName
        return url

    elif geneName[:1] == "Z":
        #Escherichia coli O157:H7 EDL933
        url = "http://www.genome.jp/dbget-bin/www_bget?" + "ece:" + geneName
        return url
    else:
        url = "none"
        return url

"""
Method for finding and extracting applicable website elements
"""

def getSequences(inputGene, browser):

    url = returnUrl(inputGene)
    if url == "none":
        return ["none","none"]

    browser.get(url)
    geneSeq = ""
    proteinSeq = ""

    count = 30
    found = False
    while count != 1 :
        string = "html/body/div[1]/table/tbody/tr/td/table[2]/tbody/tr/td[1]/form/table/tbody/tr/td/table/tbody/tr["+str(count)+"]/td"
        string2 = "html/body/div[1]/table/tbody/tr/td/table[2]/tbody/tr/td[1]/form/table/tbody/tr/td/table/tbody/tr["+str(count-1)+"]/td"
        try:
            gS = browser.find_element_by_xpath(string).text
            gS = gS[gS.find('\n')+1:]
            for char in gS:
                if char.isalpha():
                    geneSeq = geneSeq + char

            pS = browser.find_element_by_xpath(string2).text
            pS = pS[pS.find('\n')+1:]
            for char in pS:
                if char.isalpha():
                    proteinSeq = proteinSeq + char
            found = True
            break
        except:
            count = count - 1

    if found == False:
        geneSeq = "none"
        proteinSeq = "none"
        return [geneSeq,proteinSeq]
    else:
        return [geneSeq,proteinSeq]

##run the program

#browser = webdriver.Firefox(executable_path='C:/Users/egrab/Documents/catg/project/lib/geckodriver.exe') # can use firefox
r = open('final_blast_Table.txt', "r")

browser = ""
w = ""
lines = r.readlines()
count  = 0
linesDone = 0 #can start at any line
print(datetime.datetime.now(), end='')
print(" Program Start Time")

while linesDone < len(lines):
    if count == 0:
        w = open("EcsResults.txt", "a") #open file to append
        browser = webdriver.PhantomJS()
    temp = lines[linesDone].split("\t")
    probe = temp[0].strip()
    inputGene = temp[1].strip()
    a = getSequences(inputGene, browser)
    w.write(probe + "\t" + inputGene + "\t" + a[0] + "\t"+ a[1] +"\n")
    count = count + 1
    linesDone = linesDone + 1

    if count == 500:  # due to the machine crashing, program terminates and restarts
                    #every 500 probes
        count = 0
        w.close()
        browser.close()
        browser.quit()
        browser = ""
        time.sleep(7)
        print(datetime.datetime.now(), end='')
        print(" only " + str(linesDone) + " done")
print(datetime.datetime.now(), end='')
print(" Program End Time")
