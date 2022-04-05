import os
from dotenv import load_dotenv
from sqlobject import *
from sqlobject.mysql import builder
load_dotenv() 


db = os.getenv("MYSQL_DB")
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")


conn = builder()(
    db,
    user,
    password,
    host, 
)