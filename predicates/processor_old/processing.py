import csv
import re
import string
import nltk

def main():
    readTable('raw.csv', 'processed.csv', 'lemmas.csv')


def readTable(inputName, outputName, dictName):

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
        
        lastline = "sentence"
        verbs = "verbs"
        termList = "terms"
        
        for row in rdr:
            
            # tagging verbs
            line = row[2]
            if line!=lastline:

                wtr.writerow([lastline.replace('"', ''), verbs, termList])
                
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

            # compile the terms
            termpair = [row[0].strip('\"'),row[1].strip('\"')]
            termList.append(termpair)
                        
            #eliminate repeats from terms
            terms = row[0].strip('\"').split(':')
            
            for term in terms:
                for verb in verbs:                    
                    if term==roots[verb]:
                        verbs.remove(verb)


if __name__ == "__main__":
    main()

