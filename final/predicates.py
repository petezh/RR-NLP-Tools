import csv
import re
import string
import nltk
import os

def main():

    # specify filepaths
    tablename = "raw.csv"
    lemmapath = "tools\\lemmas.csv"
    preppath = "tools\\preps.csv"
    synpath = "tools\\synonyms.csv"
    filterpath = "tools\\filters.csv"

    execute(tablename, lemmapath, preppath, synpath, filterpath)

# execute methods
def execute(table, lemma, prep, syn, filt):
    
    getVerbs(table, 'verbs.csv', lemma)
    getTuples('verbs.csv', 'tuples.csv')
    reformat("tuples.csv", lemma, syn, prep, "formatted.csv", filt)
    getFrequencies("formatted.csv", "results.csv")

    print("Finished!")
    
    clean()

# deletes used databases
def clean():
    os.remove('verbs.csv')
    os.remove('tuples.csv')
    os.remove('formatted.csv')


# =====================
#   UTILITY FUNCTIONS
# =====================

# accepts the raw data and isolates potential verbs

def getVerbs(inputName, outputName, dictName):

    print("Getting verbs...")
    wtr = csv.writer(open(outputName,'w'), lineterminator = '\n')
    with open(inputName,'r') as f:

        # compile verb dictionary
        validWords = list()
        roots = dict()
        finder = csv.reader(open(dictName, 'r'), delimiter=",")
        next(finder)
        for forms in finder:
            validWords = validWords + forms
            for form in forms:
                roots[form] = forms[0]


        # read in phrase verb pairs
        rdr = csv.reader(f, delimiter=",")
        next(rdr)

        docID = "docID"
        lastline = "sentence"
        verbs = "verbs"
        termList = "terms"
        
        for row in rdr:
            
            # part-of-speech tagging
            line = row[2]
            if line!=lastline:
                wtr.writerow([docID, lastline.replace('"', ''), verbs, termList])
                text = nltk.word_tokenize(line)
                tagged = nltk.pos_tag(text)

                termList = list()
                origList = list()
                
                # extract verbs
                verbs = list()
                for item in tagged:
                    if (item[1] == 'VB' or item[1] == 'VBD' or item[1] == 'VBG' or item[1] ==  'VBN' or item[1] =='VBP' or item[1] == 'VBZ') and item[0].isalpha() and (item[0] in validWords):
                        verbs.append(item[0].strip())
   
                
                lastline = line

            # get doc IDs
            docID = row[3]
            
            # compile the terms
            termpair = [row[0].strip('\"'),row[1].strip('\"')]
            termList.append(termpair)
                        
            #eliminate repeats from terms
            terms = row[0].strip('\"').split(':')
            
            for term in terms:
                for verb in verbs:                    
                    if term==roots[verb]:
                        verbs.remove(verb)

    print("Done.")
    
# accepts a list of sentences and verbs and builds subject-predicate-object pairs

def getTuples(inputName, outputName):

    print("Building tuples...")
    
    output = open(outputName, 'w')
    wtr = csv.writer(output, lineterminator = '\n')
    
    rdr = csv.reader(open(inputName, 'r'), delimiter =",", skipinitialspace= True)
    next(rdr)
    
    # parse in file
    for row in rdr:

        docID = row[0]
        
        # evaluate each sentence
        sentence = row[1].translate(str.maketrans('', '', string.punctuation))
        verbs = eval(row[2])
        terms = eval(row[3])
        tuples = search(sentence, verbs, terms)

        # write to output
        for tpl in tuples:
            wtr.writerow([docID]+tpl)
            
    print("Done.")


# calls searches for different levels of terms on a sentence
def search(sentence, verbs, terms):
    
    lv1terms = list()
    lv2terms = list()
    lv3terms = list()
    
    # classify terms by level
    for term in terms:

        level = getLevel(term[0])

        if level == 1:
            lv1terms.append(term)
        if level == 2:
            lv2terms.append(term)
        if level == 3:
            lv3terms.append(term)

    # build tuples for each term
    tuples_1 = buildTuples(sentence, lv1terms, verbs, 1)
    tuples_2 = buildTuples(sentence, lv2terms, verbs, 2)
    tuples_3 = buildTuples(sentence, lv3terms, verbs, 3)

    return tuples_1 + tuples_2 + tuples_3
        
# returns the break level of a term
def getLevel(term):

    maxlevel = -1
    for element in term.split(":"):
        try:
            i = int(element)
            maxlevel = max(maxlevel, i)
        except ValueError:
            pass

    return maxlevel+1


# returns the left and right indices of a term
def getIndices(termText, sentence):

    lower = -1
    upper = -1
    
    try:
        lower = sentence.index(termText)
        upper = lower + len(termText)
    except ValueError:
        pass
    
    return (lower, upper)


# construct subject-predicate-object tuples
def buildTuples(sentence, terms, verbs, level):

    tuples = list()
    
    beg = -1
    end = -1
    term = ""
    helpers = ['used to', 'appears to', 'will have','have','had','has','be','is','are','were','will be', 'has been']
    
    # iterate through the terms
    for term in terms:

        # get indices
        start, stop = getIndices(term[1], sentence)
        end = start
        
        # search for verbs between terms
        if end > beg:
            for verb in verbs:
                if not sentence.find(verb, beg, end) == -1:
                    words = sentence.split()
                    wordBefore = words[words.index(verb)-1]
                    if wordBefore in helpers:
                        tuples = tuples[:-1]
                        tuples.append([sentence, lastTerm[1], lastTerm[0], wordBefore + " "+ verb, term[1], term[0], level, end-beg])
                    else:
                        tuples.append([sentence, lastTerm[1], lastTerm[0], verb, term[1],term[0], level, end-beg])
        beg = stop
        lastTerm = term
        
    return tuples


# accepts a list of tuples and adds roots and synonyms
def reformat(fileName, dictName, synName, prepName, outputName, filterName):

    print("Reformatitng...")

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

        # build a reverse synonyms dictionary
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

    # build a prepositions dictionary
    finder = csv.reader(open(prepName, 'r'), delimiter=",")
    next(finder)

    preps = list()
    for prep in finder:
        preps.append(prep[0])

    # collect filters
    finder = csv.reader(open(filterName, 'r'), delimiter=",")
    filters = list()
    for filt in finder:
        filters.append(filt[0])

    
    
    wtr = csv.writer(open(outputName, 'w'), lineterminator = '\n')

    # headings
    wtr.writerow(["docID", "sentence","subject","predicate", "object", "root", "synonyms", "level", "distance"])

    # make nice columns
    for row in rdr:
        docID = row[0]
        sentence = row[1]
        subject = row[2]
        subterm = row[3]
        obj = row[5]
        objterm = row[6]
        level = row[7]
        distance = row[8]
        fullverb = row[4]
        verb = fullverb.split()[-1]
        root = roots[verb]
        
        syn = set()


        # grab preps
        words = sentence.split()
        
        wordbefore = words[words.index(fullverb.split()[0])-1]
        if wordbefore.strip() in preps:
            fullverb = wordbefore + " " + fullverb

        wordafter = words[words.index(verb)+1]
        if wordafter.strip() in preps:
            fullverb = fullverb + " " + wordafter
            
        # use sets to avoid duplicates
        for ID in synIDs[root]:
            syn.update(syns[ID])

        # write to output
        if not fullverb in filters:
            wtr.writerow([docID, sentence, subject, fullverb, obj, root, syn, level, distance, subterm, objterm])
        
    print("Done.")

# counts frequencies and recompile database
def getFrequencies(fileName, outputName):

    print("Getting frequences...")
        
    rdr = csv.reader(open(fileName, 'r'), delimiter =",", skipinitialspace= True)
    next(rdr)

    predFreqs = dict()
    rootFreqs = dict()
    subFreqs = dict()
    objFreqs = dict()

    # counting frequencies
    for row in rdr:


        # count predicate freqs
        predicate = row[3]
        if predicate in predFreqs:
            predFreqs[predicate] += 1
        else:
            predFreqs[predicate] = 1

        # count root freqs
        root = row[5]
        
        if root in rootFreqs:
            rootFreqs[root] += 1
        else:
            rootFreqs[root] = 1

        # count subject freqs
        sub = row[2]
        if sub in subFreqs:
            subFreqs[sub] += 1
        else:
            subFreqs[sub] = 1

        # count obj freqs
        obj = row[4]
        if obj in objFreqs:
            objFreqs[obj] += 1
        else:
            objFreqs[obj] = 1
        

    rdr = csv.reader(open(fileName, 'r'), delimiter =",", skipinitialspace= True)
    next(rdr)

    wtr = csv.writer(open(outputName, 'w'), lineterminator = '\n')    

    # headings
    wtr.writerow(["subject", "object", "predicate", "sentence", "pred freq", "sub freq", "obj freq", "distance", "root", "root freq", "synonyms", "sub term","obj term", "level", "doc ID"])

    # write columns
    
    for row in rdr:
        
        docID = row[0]
        sentence = row[1]
        subject = row[2]
        subfr = subFreqs[subject]
        predicate = row[3]
        predfr = predFreqs[predicate]
        obj = row[4]
        objfr = objFreqs[obj]
        root = row[5]
        synonyms = row[6]
        level = row[7]
        distance = row[8]
        subterm = row[9]
        objterm = row[10]
        rootfr = rootFreqs[root]
        
        wtr.writerow([subject, obj, predicate, sentence, predfr, subfr, objfr, distance, root, rootfr, synonyms, subterm, objterm, level, docID])

    print("Done")


if __name__ == "__main__":
    main()
