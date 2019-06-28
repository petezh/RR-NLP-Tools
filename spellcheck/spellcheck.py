#
# The spellchecker makes use of the SymSpellPy library.
#
# Install the symspellpy module with:
# pip install -U symspellpy
#

import csv
from symspellpy.symspellpy import SymSpell, Verbosity
import re

def main():

    filePath = "raw.csv"
    outPath = "checked.csv"
    omitPath = "omit.csv"
    freqPath = "tools\\frequencies.txt"
    dictPath = "tools\\dict.txt"
    
    spellCheck(filePath, freqPath, outPath, omitPath, dictPath, 0, 1, 2)
    
def spellCheck(filePath, freqPath, outPath, omitPath, dictPath, termCol, origCol, sentCol):

    sym_spell = SymSpell(3, 7)
    sym_spell.load_dictionary(freqPath, 0, 1)

    file = open(filePath, 'r')
    fileReader = csv.reader(file, delimiter = ",")
    
    omitFile = open(omitPath, 'r')
    omitReader = csv.reader(omitFile)

    omissions = set()
    next(omitReader)
    for row in omitReader:
        omissions.add(row[0].strip())


    dictionary = set()
    dictFile = open(dictPath, 'r')
    for word in dictFile:
        dictionary.add(word.strip())


        
    outfile = open(outPath, 'w')
    outWriter = csv.writer(outfile, lineterminator = '\n')
    outWriter.writerow(["term", "original", "sentence", "docID"])

    numUp = 0
    numCor = 0
        
    next(fileReader)
    for row in fileReader:

        term = row[termCol]
        orig = row[origCol]
        sentence = row[sentCol]
        words = term.split(":")
        title = False


        
        
        for i in range(len(words)):

            word = words[i]

            # try to get index
            try:
                index = sentence.lower().split().index(word)
                orig = sentence.split()[index]
            except:
                index = -1
                orig = ""


            # check if first word of sentence
            firstWord = index == 0

            # word characters only and sufficiently long
            if word.isalpha() and len(word) > 4:

                if not firstWord and (orig.istitle() or orig == word.upper()):

                        #print(word)
                        numUp += 1
                            
                        word = word.upper()
                        title = True

                
                # if incorrect
                elif not word.lower() in dictionary:
                    
                    # if it's a title, make uppercase and collate
                    if title:

                        #print(word)
                            
                        word = word.upper()
                        title = True

                    elif not word in omissions:

                        # try to find a replacement
                        fixes = sym_spell.lookup(word, Verbosity.TOP, 1)
                        if(len(fixes) > 0):

                            #print(word + " -> " + fixes[0].term + "\n")
                            numCor += 1

                            word = fixes[0].term
                                   

                elif title:

                    # end title sequence
                    title = False
                        
        
        row[0] = ":".join(words)
        
        outWriter.writerow(row)


    print("Identified " + str(numUp) + " titles and " + str(numCor) + " misspellings.")


if __name__ == "__main__":
    main()
