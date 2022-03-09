from sqlobject import *
from sqlobject.mysql import builder

conn = builder()(
    'test',
    'root',
    'password',
    '192.168.188.164', 
    )