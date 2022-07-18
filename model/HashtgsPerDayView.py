from sqlobject.views import *
from model.Hashtags import Hashtag
from utils.mysql import *

class HashtgsPerDayView(ViewSQLObject):
    _connection = conn

    date = DateTimeCol(dbName= Hashtag.q.created)
    tag = StringCol(dbName=Hashtag.q.text)
    total = IntCol(dbName=func.COUNT(Hashtag.q.id))

    class sqlmeta:
        table="hashtags_metadata"