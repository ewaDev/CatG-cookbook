"""
Scrip for accessing the SignalP website, entering data and
retrieving results
Date: 08/09/2017
"""

from selenium import webdriver
import bs4 as bs
import urllib.request
import time
import datetime

def formatsignalPDatabase():
    noneCount = 0
    dnaCount = 0

    signalPOutput = open("signalPOutputECS2.txt", "r")
    rDB = open("EcsResults.txt", "r")
    w = open("DbEcs.txt","w")

    sP = signalPOutput.readlines()
    sDB = rDB.readlines()


    sigPdb = {}
    for i in range(len(sP)):
        temp = sP[i].split("\t")
        sigPdb.update({temp[0].strip():temp[1].strip()})

    for j in range(len(sDB)):
        result = ""
        temp = sDB[j].split("\t")

        for k in range(len(temp)):
            temp[k]  = temp[k].strip()

        if temp[2] == "none":
            dnaCount =dnaCount +1

        if temp[3] == "none":
            noneCount = noneCount+1
            result = "none"
        else:
            result = sigPdb.get(temp[0], "NO")

        w.write(temp[0] + "\t" + temp[1] + "\t" +  temp[2] + "\t" + temp[3] + "\t" + result + "\n")

    print("DNA sequences not found: " + str(dnaCount))
    print("Protein sequences not found: " + str(noneCount))

"""
Method which saves contents of the passed over link
using beautiful soup library
"""
def saveOutput(link):
    w = open("signalPOutputECS.txt","a")
    sauce = urllib.request.urlopen(link).read() #reads in the link
    soup = bs.BeautifulSoup(sauce,"lxml").get_text() #gets text from thr link
    lines = soup.split("\n")
    eof = len(lines) -1
    for i in range(len(lines)):
        if i > 2 and i < eof:
            temp = lines[i].split("\t")
            for j in range(len(temp)):
                temp[j]=temp[j].strip()
            w.write(temp[0]+"\t" +temp[8]+"\n") #saves the output to file


#Method for accessing SignalP website and inserting protein sequences

def getSelenium(sequenceInput):
    #browser = webdriver.Firefox(executable_path='C:/Users/egrab/Documents/catg/project/lib/geckodriver.exe')
    browser = webdriver.PhantomJS()

    browser.get('http://www.cbs.dtu.dk/services/SignalP/')
    time.sleep(2) #allows for the broweser to open

    #Select approperiate ratdio buttons
    radioOrg = browser.find_element_by_xpath('//input[@value="gram-"]')
    radioOrg.click()
    radioImage = browser.find_element_by_xpath('html/body/table/tbody/tr/td[2]/table[2]/tbody/tr/td/form/p[3]/table/tbody/tr[1]/td[3]/input[1]')
    radioImage.click()

    inputText = browser.find_element_by_xpath("html/body/table/tbody/tr/td[2]/table[2]/tbody/tr/td/form/p[1]/textarea")
    inputText.send_keys(sequenceInput)
    submit = browser.find_element_by_xpath("html/body/table/tbody/tr/td[2]/table[2]/tbody/tr/td/form/p[4]/input[1]")
    submit.click()
    time.sleep(150) ## this allows for the requests to be processed at SignalP end  ~2min min
    link = ""
    ## once signalP is finshed with processing, results are passed to Beautiful soup fpr scraping
    try:
        link = browser.find_element_by_xpath("/html/body/pre/pre/a[2]")
        link = link.get_attribute("href")
    except:
        print("finding link did not work")

    browser.close()
    browser.quit()
    browser = ""
    saveOutput(link) ##save output to file

def start():
    print(datetime.datetime.now(), end='')
    print(" Program Start Time")
    r = open("EcsResults - Copy.txt", "r")
    w = open("signalPOutputECS2.txt","w")
    w.write("Probe\tSignal\n")
    w.close()

    count = 0
    iteration = 1
    fileInput = r.readlines()
    probes = ""
    eof = len(fileInput)-1
    for i in range(len(fileInput)):
        temp = fileInput[i].split("\t")
        for j in range(len(temp)):
            temp[j]=temp[j].strip()

        line = ">" + temp[0] + "\n" + temp[3] + "\n" #changes to FASTA format
        probes = probes + line
        count = count + 1
        if count == 500 or i == eof:
            if count == 500:
                print(datetime.datetime.now(), end='')
                print("Scraping data: Iteration " + str(iteration))
                iteration = iteration + 1
            getSelenium(probes)
            probes = ""
            count = 0;
    print(datetime.datetime.now(), end='')
    print(" Program Finish Time")

start()
