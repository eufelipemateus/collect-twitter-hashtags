from model.Collects import Collect
from model.Tweet import Tweet 
from model.Hashtags import Hashtag
from model.UserMention import UserMention
from model.Woeids import Woeid

import csv

"""
if not(UserMention.tableExists()):
    UserMention.createTable()
if not(Tweet.tableExists()):
    Tweet.createTable()
"""
if not(Collect.tableExists()):
    Collect.createTable()
if not(Woeid.tableExists()):
    Woeid.createTable()
    with open('woeid.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:            
            p = Woeid(
                country = row[0],
                woeid = int(row[1]),
                code  = row[2]
            )
if not(Hashtag.tableExists()):
    Hashtag.createTable()
               
print("executado com sucesso!")