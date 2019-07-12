# processing
import operator
from operator import methodcaller
import csv
import re
import numpy as np
import pandas as pd
from pprint import pprint
import string
import math
import itertools
import sqlite3

# gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.models import HdpModel
from gensim.models import TfidfModel

# plotting tools
import pyLDAvis
import pyLDAvis.gensim
import matplotlib.pyplot as plt

# sci-kit
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import feature_extraction



resultFile = open("results.csv",'a')
results = csv.writer(resultFile,lineterminator ='\n')


def main():
    execute(10, 8)
    
def execute(passes, topics):
    
    con = sqlite3.connect("topics.db")
    cur = con.cursor()

    print("Training LDA...")

    lda_model = gensim.models.LdaMulticore(corpus_tfidf, num_topics=topics, id2word=dictionary, passes=passes, workers =4)
    print("Done.")
    
    print("Writing topics to terms...")
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS TERMS
            (topic INT,
            term TEXT,
            prob FLOAT)
    """)
    
    for i in range(lda_model.num_topics):
        topics = lda_model.show_topic(i, topn = 20)
        for t in topics:
            cur.execute("INSERT INTO TERMS (topic, term, prob) VALUES (?, ?, ?)", [i+1, t[0], t[1]])


    print("Done.")
    print("Writing doc to topics...")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS DOCS
            (doc TEXT,
            topic INT,
            prob FLOAT)
    """)
    
    for ID in docIDs:

        doc = docTokens[ID]
        store = list(lda_model[dictionary.doc2bow(doc)])

        for pair in store:
            
            cur.execute("INSERT INTO DOCS (doc, topic, prob) VALUES (?, ?, ?)", [docID, pair[0], pair[1]])
        
    print("Done.")

# preprocessing
blFile= open("tools\\blacklist.csv", 'r')
blacklist = [t.strip() for t in next(csv.reader(blFile))]
blFile.close()
levels = [1, 2, 3]

# format [term, orig, sentence, docID]
inPath = "raw.csv"

inFile = open(inPath, 'r')
inReader = csv.reader(inFile)

docTokens = dict()

# ignore headers
next(inReader)

for inRow in inReader:
    
    term = inRow[0]
    sentence = inRow[2]
    docID = inRow[3]
    
    # find acceptable tokens only
    token = "_".join([t for t in term.split(":") if re.match(r'[^\W\d]*$', t) and not t in blacklist])
    
    # calculate new term level
    level = token.count("_")
    
    # if acceptable, add to dictionary
    if level in levels and not token in blacklist and len(token) > 0:
        if docID in docTokens:
            docTokens[docID] += [token]
        else:
            docTokens[docID] = [token]

docIDs = list(docTokens.keys())
texts= list(docTokens.values())

dictionary = corpora.Dictionary(texts)

dictionary.filter_extremes(no_below=3, no_above=1, keep_n=10000)
corpus = [dictionary.doc2bow(text) for text in texts]


tfidf = TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]




if __name__ == "__main__":
    main()
    
