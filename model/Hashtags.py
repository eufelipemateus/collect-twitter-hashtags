from sqlobject import *
from utils.mysql import *

class Hashtag(SQLObject):
    _connection = conn
    collect = ForeignKey('Collect')
    position = IntCol()
    text = StringCol()
    url= StringCol()
    location = ForeignKey('Woeid')
    created = DateTimeCol()
