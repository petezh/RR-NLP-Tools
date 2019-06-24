import csv

# parse through both files, build dictionaries
def read_file(fobj):
    data = {}
    for line in csv.reader(fobj):
        data[line[0]] = line[1:]
    return data

def read_file2(fobj):
    data = {}
    for line in csv.reader(fobj):
        data[line[0]+line[1]] = line
    return data

with open('dict.txt') as f1, open('pairs.txt') as f2:
    data1 = read_file2(f1)
    data2 = read_file(f2)


with open('res.txt', 'w') as result:
    wtr= csv.writer(result)

    # if the verbs match, combine the rows and write to output
    for key in data1.keys():
        try:
            key2 = key[:-1]
            wtr.writerow((data1[key][0], data1[key][1], data1[key][2], data2[key2][0], data2[key2][1], data2[key2][2], data2[key2][3], data2[key2][4], data2[key2][5], data2[key2][6], data2[key2][7], data2[key2][8], data2[key2][9], data2[key2][10]))
        except KeyError:
            pass
