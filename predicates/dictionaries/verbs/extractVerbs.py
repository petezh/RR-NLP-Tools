import sqlite3
import pandas as pd
import csv

con = sqlite3.connect("data.db")
cur = con.cursor()

# process the wordnet file
for line in open("dict.sql","r"):
    print(line)
    cur.execute(line)


# convert to csv
pd.read_sql(sql='SELECT * FROM wn_synset', con=con).to_csv("dict_csv", index=False, sep=',', quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8-sig')

con.commit()
cur.close()
con.close()





    
    


