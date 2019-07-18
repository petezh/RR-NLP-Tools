import csv
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import feature_extraction

def main():
    execute("data\\topics_init10_rat0.1_res_0.5.csv")

def thin(topicPath):

    newDict = dictionary.token2id
    length = len(dictionary)

    topicFile = open(topicPath, 'r')
    topicReader = csv.reader(topicFile)

    next(topicReader)
    next(topicReader)


    currentTopic = 0
    topicNumber = 0

    topic2term = dict()

    for row in topicReader:
        
        term = row[3]
        p = row[4]
        index = newDict[term]
        
        if not row[2] == currentTopic:
            currentTopic = row[2]
            topicNumber += 1
            topic2term[topicNumber] = [0]*length
            
            topic2term[topicNumber][index] = [index, p]
        else:
            topic2term[topicNumber][newDict[term]] = [index, p]

    topicNums = topic2term.keys()

    for t1, t2 in itertools.combinations(topicNums, 2):
        cs = cosine_similarity(topic2term[t1], topic2term[t2])
        if cs > 0.005:
            print(cs)
    
    
    
