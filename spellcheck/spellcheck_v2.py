#
# The spellchecker makes use of the SymSpellPy library.
#
# Install the symspellpy module with:
# pip install -U symspellpy
#

import csv
from symspellpy.symspellpy import SymSpell, Verbosity
import re
import string

def main():

    filePath = "raw.csv"
    outPath = "checked.csv"
    fixesPath = "fixes.csv"
    omitPath = "omit.csv"
    freqPath = "tools\\frequencies.txt"
    dictPath = "tools\\dict_combined.txt"
    
    spellCheck(filePath, freqPath, fixesPath, outPath, omitPath, dictPath)

    
def spellCheck(filePath, freqPath, fixesPath, outPath, omitPath, dictPath):

    file = open(filePath, 'r')
    fileReader = csv.reader(file, delimiter = ",")

    print("Loading dictionaries...")

    # build spell fixer
    sym_spell = SymSpell(3, 7)
    sym_spell.load_dictionary(freqPath, 0, 1)

    # build omissions
    omitFile = open(omitPath, 'r')
    omitReader = csv.reader(omitFile)

    omissions = set()
    next(omitReader)
    for row in omitReader:
        omissions.add(row[0].strip())

    # build dictionary
    dictionary = set()
    dictFile = open(dictPath, 'r')
    for word in dictFile:
        dictionary.add(word.strip())

    # create cleaned output
    outfile = open(outPath, 'w')
    outWriter = csv.writer(outfile, lineterminator = '\n')
    outWriter.writerow(["term", "original", "sentence", "docID"])

    # create change log
    fixFile = open(fixesPath, 'w')
    fixWriter = csv.writer(fixFile, lineterminator = '\n')
    fixWriter.writerow(["orig", "new", "sentence"])

    # counter
    numCor = 0

    print("Searching file...")
    
    next(fileReader)
    for row in fileReader:
        
        term = row[0]
        orig = row[1]
        sentence = row[2]
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        words = term.split(":")
        title = False
        spellError = False
        
        for i in range(len(words)):

            word = words[i]

            # try to get index
            try:
                index = sentence.lower().split().index(word)
                orig = sentence.split()[index]
            except:
                index = -1
                orig = ""
                

            # word characters only and sufficiently long
            if word.isalpha() and len(word) > 4 and not word in omissions and not word in dictionary:
                if (word+"s") in sentence.lower().split() and index == -1:
                        words[i] += "s"
                        numCor += 1
                        print("changed "+word + " to " + word+"s")
                elif not index == -1 and (orig.islower() or index == 0):
                    fixes = sym_spell.lookup(word, Verbositsy.TOP, 1)
                
                    if(len(fixes) > 0) and not fixes[0].term == word and fixes[0].term in dictionary:
                        words[i] = fixes[0].term
                        numCor += 1
                        print("changed "+word + " to " + fixes[0].term)
                                
                        
        newTerm = ":".join(words)        
        if not term == newTerm:
            fixWriter.writerow([term, newTerm, sentence])
            term = newTerm

        outWriter.writerow(row)

    print("Done")
    
    print("Identified " + str(numCor) + " misspellings.")


if __name__ == "__main__":
    main()
