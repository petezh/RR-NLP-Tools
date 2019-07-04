import subprocess, csv, time
import requests

def main():

    #getDOIs("missed.csv", "outputs.txt")
    getURLs("DOIs.txt", "URLs.txt")

def getDOIs(inPath, outPath):

    inFile = open(inPath, 'r')
    inReader = csv.reader(inFile)
    IDList = []

    for row in inReader:
        IDList.append(row[0])
    outFile = open(outPath, 'w')

    for ID in IDList:
        
        output = subprocess.check_output("curl \"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=" + str(ID) + "&retmode=json\"")
        
        string = "".join(map(chr, output))
        startDOI = string.find("doi")
        start = string.find("value", startDOI)
        end = string.find("\"", start + 9)
        outFile.write(string[start+9:end:] + "\n")
        print(string[start+9:end:])
        time.sleep(0.5)

def getURLs(inPath, outPath):

    inFile = open(inPath, 'r')
    outFile = open(outPath, 'w')

    for DOI in inFile:
        r = requests.get("https://doi.org/" + DOI) 
        outFile.write(r.url)


if __name__ == "__main__":
    main()
