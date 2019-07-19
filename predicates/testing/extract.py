import csv, re, string, sys

csv.field_size_limit(1000000)

with open("parmenides.csv", 'r') as inFile, open("test.csv", 'w') as outFile:

    outWriter = csv.writer(outFile, lineterminator = "\n")

    next(inFile)

    outWriter.writerow(["term", "orig", "sentence", "ID"])

    counter = 1
    
    IDcount = 1
    IDmap = dict()
    
    for i in range(0, 200):

        try:
            row = next(csv.reader([next(inFile)], quoting=csv.QUOTE_NONE))
            
            

            outWriter.writerow(row)


        except Exception:
            print("Done!")
            break
        
