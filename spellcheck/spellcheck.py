import csv
from symspellpy.symspellpy import SymSpell, Verbosity

def main():

    filePath = "raw.csv"
    freqPath = "dictionary.txt"
    outPath = "checked.csv"
    omitPath = "omit.csv"
    dictPath = "words_alpha.txt"
    
    spellCheck(filePath, freqPath, outPath, omitPath, dictPath)
    
def spellCheck(filePath, freqPath, outPath, omitPath, dictPath):

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

    
    next(fileReader)
    for row in fileReader:

        term = row[0]
        sentence = row[2]
        words = term.split(":")

        for i in range(len(words)):
            word = words[i]
            if word.isalpha() and (len(word) > 4) and (not word in dictionary) and (not word in omissions):
                
                fixes = sym_spell.lookup(word, Verbosity.TOP, 1)
                fix = word
                if(len(fixes) > 0):
                    if not isChemical(word):
                        
                        fix = fixes[0].term
                if not fix == word:
                    words[i] = fix
                    print(word + " -> " + fix + "\n" + sentence + "\n")

        row[0] = ":".join(words)

        outWriter.writerow(row)
                        
def isChemical(word):
    return word.endswith(("yl", "ane", "ene", "ide", "ate", "ite", "ioul", "ine", "ase", "ox", "ion", "amino", "one", "ido")) or word.startswith(("bio", "di", "chro", "pyr", "non")) or ("chiral") in word 
                                                                                                    


if __name__ == "__main__":
    main()