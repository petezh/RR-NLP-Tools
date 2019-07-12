import csv, re, string

with open("allitems.csv", 'r', encoding="utf8", errors='ignore') as file, open("input.csv", 'w') as out:
    reader = csv.reader(file)
    writer = csv.writer(out, lineterminator = '\n')
    
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    
    writer.writerow(["snippet", "ID"])

    pattern = re.compile('[^A-Za-z0-9 ]')

    count = 1
    
    for row in reader:
        count += 1 
        ID = row[0]
        
        snip = pattern.sub('', row[2])
        
        writer.writerow([snip, ID])

    print("done")
