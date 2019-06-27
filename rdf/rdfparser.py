import rdflib
from rdflib import Graph, Literal
import csv

def main():

    inputName = "results.csv"
    outputName = "graph.rdf"

    parse(inputName, outputName)

def parse(inputName, outputName):

    rdr = csv.reader(open(inputName, 'r'))

    web = rdflib.Graph()

    
    next(rdr)
    for row in rdr:
        subj = Literal(row[0])
        obj = Literal(row[1])
        pred = Literal(row[2])

        web.add((subj, obj, pred))


    print(web.serialize(format = 'ntriples'))

if __name__ == "__main__":
    main()
