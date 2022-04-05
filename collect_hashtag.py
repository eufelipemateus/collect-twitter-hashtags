import logging
from datetime import *
from dateutil import parser

from utils.twitter import Conn
from utils.console import color
from model.Hashtags import Hashtag
from model.Woeids import Woeid
from model.Collects import Collect
from twitter.error import TwitterError


def collect_hashtag():
    NowDate = datetime.now()
    print(f'{color.BOLD }{color.GREEN}[Collecting data from Twitter...]{color.END} {color.END} \n')
    print(f'{color.BLUE} Started at: {str(NowDate)} {color.END} \n')
    print(f'-----------------------------------------------------\n')

    CollectObj = Collect(collected_started= NowDate)
    for WoeidObject in Woeid.select():
    
        logging.info(f'Tring get trends from {WoeidObject.country}.')
        try:
            TwitterTrends =   Conn(). GetTrendsWoeid(WoeidObject.woeid)

            for index, HahTagTrend in enumerate(TwitterTrends):
                Hashtag(
                    text= HahTagTrend.name,
                    created= parser.parse(HahTagTrend.timestamp),
                    position = HahTagTrend.tweet_volume,
                    url= HahTagTrend.url,
                    collectID= CollectObj.id,
                    locationID= WoeidObject.id
                )
                CollectObj.set(count_hashtag = CollectObj.count_hashtag + 1)
            CollectObj.set(count_country = CollectObj.count_country + 1)
            logging.info(f'{color.GREEN}[OK] Was Add {index} Hashtag from {WoeidObject.country} {color.END} ')
        except TwitterError as e:
            logging.error(f'{color.RED}Error on Twitter Api while trying to get trends from {WoeidObject.country}. {color.END}') 
            logging.debug(e)
            CollectObj.set(count_twitter_error = CollectObj.count_twitter_error + 1)
        except Exception as ae:
            logging.error(f'{color.RED}It is not possiblie get data from {WoeidObject.country}.{color.END}')
            logging.debug(ae)
            CollectObj.set(count_runtime_error = CollectObj.count_runtime_error + 1)
    NowDate = datetime.now()
    CollectObj.set(collected_ended= NowDate)
    print(f'-----------------------------------------------------\n')
    print(f'{color.YELLOW} Finished at: {str(NowDate)} {color.END} \n\n\n')
    print(f'{color.PURPLE}  Thank you!! Bye! {color.END} \n')
