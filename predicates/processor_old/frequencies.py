import csv


def main():
    getFrequencies("results.csv", "resultsfreq.csv")


def getFrequencies(fileName, outputName):

    rdr = csv.reader(open(fileName, 'r'), delimiter =",", skipinitialspace= True)
    next(rdr)

    predFreqs = dict()
    rootFreqs = dict()

    # counting frequencies
    for row in rdr:

        predicate = row[1]
        if predicate in predFreqs:
            predFreqs[predicate] += 1
        else:
            predFreqs[predicate] = 1

        root = row[3]
        
        if root in rootFreqs:
            rootFreqs[root] += 1
        else:
            rootFreqs[root] = 1


    rdr = csv.reader(open(fileName, 'r'), delimiter =",", skipinitialspace= True)
    next(rdr)

    wtr = csv.writer(open(outputName, 'w'), lineterminator = '\n')

    # headings
    wtr.writerow(["sentence", "subject","predicate","pred freq", "object", "root","root freq", "synonyms"])
    
    # writing frequencies
    for row in rdr:
        predicate = row[1]
        row.insert(2, predFreqs[predicate])
        root = row[4]
        row.insert(5, rootFreqs[root])
        wtr.writerow(row)
    
if __name__ == "__main__":
    main()
