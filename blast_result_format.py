"""
Script for formating the blast results
( from the original thesis)
Author: Ewa G
Date: 08/09/2017
"""

from decimal import *

# open the blasted file
firstBlastResult= open("blast_result.txt", "r")

#remove duplicate lines
duplicatesRemoved = open("Duplicate_Lines_removed.txt", "w")
lines_seen = set() # holds lines already seen

for line in firstBlastResult:
	if line not in lines_seen: # not a duplicate
		duplicatesRemoved.write(line)
		lines_seen.add(line)
duplicatesRemoved .close()

#tables
finalblastResults=[]
infile= "Duplicate_Lines_removed.txt"
outfile= "final_blast_Table.txt"

ifh=open(infile) # input file
curr=''
for line in ifh.readlines():
    row=line.strip().split()
    if row[0] != curr:
        #ofh.write(line)
        curr=row[0]
        finalblastResults.append(row)
ifh.close()

matchedLenght = 50
maxAlignmentError = 5
identity = 95.00

filteredResults = filter(lambda x: int(x[3]) >= matchedLenght and int(x[4]) <= maxAlignmentError and Decimal(x[2]) >= identity, finalblastResults)
header=["query name","subject","percent identities","aligned length","number of mismatched positions","number of gap positions","query sequence start","query sequence end","subject sequence start","subject sequence end","e-value","bit score"]
with open(outfile, 'w') as i:
    i.write("\t".join(header)+"\n")
    for item in filteredResults:
        item = "\t".join(item)
        i.write(item+'\n')
