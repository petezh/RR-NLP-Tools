import subprocess, csv

inFile = open("missed.csv", 'r')
inReader = csv.reader(inFile)
IDList = []
for row in inReader:
    IDList.append(row[0])
outFile = open("outputs.txt", 'w')


for ID in IDList:
    
    output = subprocess.check_output("curl \"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=" + str(ID) + "&retmode=json\"")
    
    string = "".join(map(chr, output))
    startDOI = string.find("doi")
    start = string.find("value", startDOI)
    end = string.find("\"", start + 9)
    outFile.write(string[start+9:end:] + "\n")
