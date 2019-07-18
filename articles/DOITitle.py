
import sys
import urllib.request
from urllib.error import HTTPError
import csv


BASE_URL = 'http://dx.doi.org/'

def main():

    rdr = csv.reader(open("raw.csv", 'r'))


    # DOI should be in the format 10.1107/S####...
    for row in rdr:
        print(getTitle(row[3]))


def getTitle(doi):
    url = BASE_URL + doi
    req.add_header('Accept', 'application/x-bibtex')
    try:
        with urllib.request.urlopen(req) as f:
            bibtex = f.read().decode()
        start = bibtex.find("title = {")
        end = bibtex.find("},", start)
        return bibtex[start + 9:end]
        
        
    except HTTPError as e:
        if e.code == 404:
            return('DOI not found.')
        else:
            return('Service unavailable.')


if __name__ == "__main__":
    main()
