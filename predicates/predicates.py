import csv
import re
import string

wtr = csv.writer(open('predicates.txt','w'))


with open('tagged.txt','r') as f:


    rdr = csv.reader(open('raw.csv','r'), delimiter=",")

    
    count = 0
    for line in f:
        if count%4==0:
            sentence = line.strip('\"')
            
        if count%4==2:

            verbs = line.strip().split(",")[1:]

            


            row = next(rdr)
            print(row[0])
            print(sentence)
                                                    
            # remove accidental verbs
            while row[0].strip('\"').split()[0]==sentence.split()[0] and row[1].strip('\"').split()[1]==sentence.split()[1] and row[1].strip('\"').split()[1]==sentence.split()[2]:
                terms = row[1].strip('\"').split()
                
                
                for term in terms:
                    
                    for verb in verbs:
                        if term==verb:
                            verbs.remove(verb)

                row = next(rdr)
            sentence = sentence.translate(str.maketrans('', '', string.punctuation))
            wordlist = sentence.split()

                        
            
        count = count+1
