import nltk
import csv

tagwtr = csv.writer(open('tagged.txt', 'w'))

# tagger

with open("testdata.txt", 'r') as f:
    i=0
    for line in f:
        text = nltk.word_tokenize(line)
        tagged = nltk.pos_tag(text)


        verbs = list()
        for item in tagged:
            if item[1] == 'VB' or item[1] == 'VBD' or item[1] == 'VBG' or item[1] ==  'VBN' or item[1] =='VBP' or item[1] == 'VBZ':

                verbs.append(item[0].strip())

        verbs.insert(0, line)
        tagwtr.writerow(verbs)
        print(i)
        i = i+1
