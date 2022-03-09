from sqlobject import *
from mysql import *


class UserMention(SQLObject):
    _connection = conn
    username = StringCol()
    created = DateTimeCol()