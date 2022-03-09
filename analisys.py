import json
from datetime import *
from mysql import *

from collections import Counter
import re

from model.Tweets import Tweet 
from model.Hashtag import Hashtag
from model.UserMention import UserMention

NowDate = datetime.now()
OneHourAgo = NowDate - timedelta(hours=1, minutes=0)

reg = re.compile('\S{4,}')

select_string = ""
wordsAll = ""
wordsFinal = []


if OneHourAgo:
    select_string +=' created '+ "   BETWEEN"  + '"' + str(OneHourAgo)  + '"'
if NowDate:
    select_string += " AND " + '"' + str(NowDate) + '"'

query = Tweet.select(select_string)

""" d """
for d in query:
    sentence =Counter(ma.group() for ma in reg.finditer(d.text))
    for word in sentence:
        wordsAll += word+ " " 

""" K """
wordsFinal = Counter(ma.group() for ma in reg.finditer(wordsAll))
print(wordsFinal)

pretty_object = json.dumps(wordsFinal, indent=4)
print(pretty_object)


