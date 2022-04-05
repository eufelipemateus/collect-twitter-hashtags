from sqlobject import *
from utils.mysql import *


class Tweet(SQLObject):
    _connection = conn
    text = StringCol()
    created = DateTimeCol()
    lang = StringCol(length=2)