from sqlobject import *
from utils.mysql import *

class Collect(SQLObject):
    _connection = conn
    count_country = IntCol(default=0)
    count_hashtag = IntCol(default=0)
    count_twitter_error = IntCol(default=0)
    count_runtime_error =   IntCol(default=0)
    collected_started = DateTimeCol()
    collected_ended = DateTimeCol(default=None)
    hashtags = MultipleJoin('Hashtag')
