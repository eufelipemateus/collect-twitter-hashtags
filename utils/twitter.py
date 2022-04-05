
from dotenv import load_dotenv
import twitter
import os

load_dotenv() 

CunsumerKey = os.getenv("CONSUMER_KEY")
ConsumerSecret = os.getenv("CONSUMER_SECRET")
AccessTokenKey = os.getenv("ACCESS_TOKEN_KEY")
AccessTokenSecret = os.getenv("ACCESS_TOKEN_SECRET")

###

def Conn():
    return twitter.Api(
        consumer_key= CunsumerKey,
        consumer_secret= ConsumerSecret,
        access_token_key=AccessTokenKey,
        access_token_secret=AccessTokenSecret,
        sleep_on_rate_limit=True
    )