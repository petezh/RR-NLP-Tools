import csv
import re
import string
import nltk




readTable('raw.csv', 'predicates.txt')

def readTable(inputName, outputName):

    wtr = csv.writer(open(outputName,'w'))
    
    with open(fileName,'r') as f:
        
        rdr = csv.reader(f, delimiter=",")
        
        count = 0

        lastline = ""
        verbs = list()
        
        
        for row in rdr:
            
            #tagging
            line = row[2]
            if line!=lastline:
                verbs.insert(0, lastline.replace('"', ''))
                wtr.writerow(verbs)
                
                text = nltk.word_tokenize(line)
                tagged = nltk.pos_tag(text)

                #extract verbs
                verbs = list()
                for item in tagged:
                    if (item[1] == 'VB' or item[1] == 'VBD' or item[1] == 'VBG' or item[1] ==  'VBN' or item[1] =='VBP' or item[1] == 'VBZ') and item[0].isalpha():
                        verbs.append(item[0].strip())

                lastline = line

                        
            #eliminate repeats from terms
            terms = row[0].strip('\"').split(':')
            for term in terms:
                for verb in verbs:
                    if term==verb:
                         verbs.remove(verb)




