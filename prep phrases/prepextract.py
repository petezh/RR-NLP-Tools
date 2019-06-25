
## Access files

from os import listdir
from os.path import isfile, join
mypath = "C:\\Users\\pjz1\\Downloads\\SHIP-2019-master\\prep phrases\\preps"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

import csv
import re

## Prepare output file
wtr = csv.writer(open('allPreps.txt', 'w'))
for file in onlyfiles:

    path = "C:\\Users\\pjz1\\Downloads\\SHIP-2019-master\\prep phrases\\preps\\"+file

    with open(path, 'r') as f:
        
        last = f.readline()

        for line in f:

            ## Last line is empty, only print second to last            
            secondLast = last
            last = line

        
            words = line.split()

            ## Find where the number is
            for i in range(len(words)):
                if re.search('\d+', words[i]):
                    print(words[i])
                    index = i
                    break

            ## Split the list into two strings
            separator = " "
            prepPhrase = separator.join(words[0:index])
            usedWith = separator.join(words[index+1:])
            
            print(prepPhrase)

            ## write output
            wtr.writerow([prepPhrase, usedWith])
        
