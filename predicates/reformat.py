import csv




def main():
    reformat("tuples.csv", "lemmas.csv", "synonyms.csv")

def reformat(fileName, dictName, synName):
    
    rdr = csv.reader(open(fileName, 'r'), delimiter =",", skipinitialspace= True)

    
    validWords = list()
    roots = dict()
    syns = dict()
    synIDs = dict()

    finder = csv.reader(open(synName, 'r'), delimiter=",")
    next(finder)

    # build a synonyms dictionary
    for pairs in finder:
        if pairs[0] in syns:
            syns[pairs[0]].append(pairs[1])
        else:
            syns[pairs[0]] = [pairs[1]]
        
        if pairs[1] in synIDs:
            synIDs[pairs[1]].append(pairs[0])
        else:
            synIDs[pairs[1]] = [pairs[0]]

        
    # build a verb forms dictionary
    finder = csv.reader(open(dictName, 'r'), delimiter=",")
    next(finder)

    for forms in finder:
        for form in forms:
            roots[form] = forms[0]

    

    wtr = csv.writer(open("results.csv", 'w'))

    wtr.writerow(["subject","predicate","object", "root","synonyms"])
    
    for row in rdr:
        
        subject = row[0]
        obj = row[2]
        level = row[3]
        verb = row[1]
        root = roots[verb]
        syn = set()
        for ID in synIDs[root]:
            syn.update(syns[ID])

        wtr.writerow([subject, verb, obj, root, syn])
        
        
if __name__ == "__main__":
    main()
