"""
Script for retrieval of data from KEGG database through an API
Author: Ewa 
Date: 08/09/2017
"""

from bioservices.kegg import KEGG
import datetime
import sys
import time
import re

"""
Method for returning the approperiate code
based on the primary accession number.
"""

def returnKey(geneName):
    ###organisms found via http://www.kegg.jp/kegg-bin/get_htext?htext=br08601.keg&query=cft073
    if geneName[:1] == "b":
        #Escherichia coli K-12 MG1655
        url = "eco:" + geneName
        return url
    elif geneName[:1] == "c":
        #Escherichia coli O6:K2:H1 CFT073
        geneName = geneName.replace("_", "")
        url = "ecc:" + geneName
        return url
    elif geneName[:1] == "E":
        #Escherichia coli O157:H7 Sakai
        url = "ecs:" + geneName
        return url

    elif geneName[:1] == "Z":
        #Escherichia coli O157:H7 EDL933
        url = "ece:" + geneName
        return url
    else:
        url = "none"
        return url

#kegg databases :
filein = 'API.txt'
fileout = "test.txt"

print(datetime.datetime.now(), end='')
print(" Program Start Time")

r = open(filein, "r")
lines = r.readlines()
r.close()

w = open(fileout, "a")
k = KEGG() #conect to the databases

"""
loop over all lines in the file and extract the relevant information
"""
for i in range(len(lines)):
    temp = lines[i].split("\t")
    probe = temp[0].strip() #probeID
    inputGene = temp[1].strip() #primary accession

    result = returnKey(inputGene) #get the KEGG specific organism nam
    if result == "none":
        #if return out of scope
        w.write(probe + "\t" + inputGene + "\t" + "none" + "\t"+ "none" +"\n")
    else:
        keggreturn = k.get(result) #query kegg
        if type(keggreturn) == int: #kegg returns an error as an integer if the query did not yeld results
            #write to file as none
            w.write(probe + "\t" + inputGene + "\t" + "none" + "\t"+ "none" +"\n")

        else:
            dna = ""
            protein = ""
            parse = k.parse(keggreturn) #returns a dictionary
            dnaParsed = parse.get("NTSEQ", "none")
            dna = re.sub("\s", "", dnaParsed) #remove any breaks in the returned string

            proteinParsed = parse.get("AASEQ", "none")
            protein = re.sub("\s", "", proteinParsed)
            w.write(probe + "\t" + inputGene + "\t" + dna + "\t"+ protein +"\n")

print(datetime.datetime.now(), end='')
print(" Program End Time")
