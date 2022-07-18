from sqlobject import *
from utils.mysql import *

class Woeid(SQLObject):
    _connection = conn
    country = StringCol()
    woeid = IntCol()
    code =StringCol(length=2)
    hashtags = MultipleJoin('Hashtag')

    class sqlmeta:
        table = "woeids"
