

def main():

    pathSci = "dict_scientific.txt"
    pathCom = "dict_common.txt"
    pathNew = "dict_refine.txt"
    
    sciDict = open(pathSci, 'r', encoding="utf8")
    comDict = open(pathCom, 'r', encoding="utf8")

    commons = set()
    for row in comDict:
        commons.add(row.strip())

    newDict = open(pathNew, 'w', encoding="utf8")
    
    for row in sciDict:
        if row.strip() not in commons:
            newDict.write(row)
        else:
            print(row)

    newDict.close()

if __name__ == "__main__":
    main()
