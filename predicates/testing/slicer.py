import csv, re, string, sys

csv.field_size_limit(1000000)

with open("parmenides.csv", 'r') as inFile, open("par_short.csv", 'w') as outFile:

    outWriter = csv.writer(outFile, lineterminator = "\n")

    next(inFile)

    outWriter.writerow(["term", "orig", "sentence", "ID"])

    counter = 1
    
    IDcount = 1
    IDmap = dict()
    
    for i in range(0, 1500000):

        try:
            row = next(csv.reader([next(inFile)], quoting=csv.QUOTE_NONE))
            
            term = row[0]
            orig = row[1]
            sentence = row[2]

            if ":" in term and orig in sentence:

                print(counter)
                counter += 1
                
                if sentence not in IDmap:
                    IDmap[sentence] = IDcount
                    IDcount += 1

                ID = IDmap[sentence]

                outWriter.writerow([term, orig, sentence, ID])


        except Exception:
            print("Done!")
            break
        
