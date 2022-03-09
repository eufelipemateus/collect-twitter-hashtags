from model.Tweets import Tweet 
from model.Hashtag import Hashtag
from model.UserMention import UserMention

if not(UserMention.tableExists()):
    UserMention.createTable()
if not(Hashtag.tableExists()):
    Hashtag.createTable()
if not(Tweet.tableExists()):
    Tweet.createTable()