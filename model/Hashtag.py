from sqlobject import *
from mysql import *

class Hashtag(SQLObject):
    _connection = conn
    text = StringCol()
    created = DateTimeCol()
