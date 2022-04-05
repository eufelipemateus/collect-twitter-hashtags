import json
import twitter
from datetime import datetime

from model.Tweet import Tweet 
from model.Hashtags import Hashtag
from model.UserMention import UserMention


def main():
    try:
        f = open('keys.json', 'r')
        data = json.load(f)
        f.close()

        api = twitter.Api(
            consumer_key=data['consumer_key'],
            consumer_secret=data['consumer_secret'],
            access_token_key=data['access_token_key'],
            access_token_secret=data['access_token_secret'])


    except:
        print('Error in authentication! \nMake sure you have all the credentials filled properly in keys.json file.')
        return

    """[
                (-22.6204549,-43.2618207,37.8),
                (-23.6815314,-46.8755064,37.8),
                (-15.721387,-48.0774483,37),
                (-3.0443101,-60.1071951, 37.8),
                (-12.901393,-38.560196,37.8)
            ]"""

    try:
        stream = api.GetStreamFilter(
            track=["#BBB", "#BBB22", "#RedeBBB"],
            languages=['pt'],
        )

        for tweet in stream:
            print(tweet)
            if( not( tweet.get('delete')) and  not( tweet.get('retweeted')) ) :
                date_time = datetime.fromtimestamp((int(tweet.get('timestamp_ms')) *  0.001))
                print(tweet.get('lang'))
                p = Tweet(
                    text=tweet.get('text'), 
                    created= datetime.fromtimestamp(datetime.timestamp(date_time)),
                    lang= tweet.get('lang')
                )


                metions = tweet.get('entities')
                hashtags = metions.get('hashtags')
                user_mentions = metions.get('user_mentions')

                print(p)
                for tag in hashtags:
                    t = Hashtag(
                        text= tag.get('text'),
                        created= datetime.fromtimestamp(datetime.timestamp(date_time))
                    )
                    print(t)

            
                for user in user_mentions:
                    u = UserMention(
                        username= user.get("screen_name"),
                        created= datetime.fromtimestamp(datetime.timestamp(date_time))
                    )

                    print(u)

    except print(0):
        print('Error! \n Make sure the username is valid.')
        return

if __name__ == "__main__":
    main()