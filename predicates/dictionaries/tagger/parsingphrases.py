import csv

wtr = csv.writer(open('results.txt', 'w'))

with open("test verbs.txt", 'r') as f1:
    i=0
    for line in f1:

        root = line.split()[0]
        freq = 0
        matches = list()
        
        # find matches        
        for word in line.split():
            if not word =="":
                f2 = open("testdata.txt", 'r')
                for line2 in f2:

                    for word2 in line2.split():
                        if word2 == word:
                            freq = freq+1
                            matches.append(line2)

        # write the root, no. of appearances, and each match
        wtr.writerow([root, freq, matches])            

        # roots processed
        print(i)
        i = i+1


