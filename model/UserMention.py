from sqlobject import *
from utils.mysql import *


class UserMention(SQLObject):
    _connection = conn
    username = StringCol()
    created = DateTimeCol()