import sqlite3

con = sqlite3.connect("data.db")
cur = con.cursor()
buildVerbTable("test verbs.csv", "verbs")
buildDataTable("testdata.csv", "data")


def buildVerbTable(in_csv, out_table):
    
    tableBuild="CREATE TABLE IF NOT EXISTS "+out_table+""" (
word VARCHAR(50),
form1 VARCHAR(50),
form2 VARCHAR(50),
form3 VARCHAR(50),
form4 VARCHAR(50),
form5 VARCHAR(50),
form6 VARCHAR(50),
form7 VARCHAR(50),
form8 VARCHAR(50),
form9 VARCHAR(50))
"""
    cur.execute(tableBuild)
    for row in csv.reader(open(in_csv, 'r')):
        cur.execute('INSERT INTO '+out_table+' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', tuple(row[1:]))

def buildDataTable(in_csv, out_table):
    tableBuild="CREATE TABLE "+out_table+""" (
sentence VARCHAR(300))
"""
    cur.execute(tableBuild)
    
    for row in csv.reader(open(in_csv, 'r')):
        cur.execute('INSERT INTO '+out_table+' VALUES (?)',[row[0]])
    
        


