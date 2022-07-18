import os
import logging
from datetime import *

from utils.console import color
from model.Hashtags import Hashtag
from model.Woeids import Woeid
from model.Collects import Collect
from datetime import datetime as d

from sqlobject.sqlbuilder import  LEFTJOINOn
import  preprocessor as  p
import matplotlib.pyplot as plt
import string
from wordcloud import WordCloud

date = d.now()
firstDayMonth = date.replace(day=1);
Hashtag._connection.debug = False
image_path = os.getenv("IMAGE_PATH")

def cloud_words():
    NowDate = datetime.now()
    print(f'{color.BOLD }{color.GREEN}[Generate WordCloud...]{color.END} {color.END} \n')
    print(f'{color.BLUE} Started at: {str(NowDate)} {color.END} \n')
    print(f'-----------------------------------------------------\n')

    for WoeidObject in Woeid.select():
        try:
            logging.info(f'Genereting wordclound from  {Woeid.q.country}.')

            file_name =  image_path + WoeidObject.code + date.strftime("-%Y-%m") + '.png'
            all_tags = []
            all_tags.extend([tag.text for tag in  Hashtag.select(
                                (Collect.q.collected_ended >= firstDayMonth) &
                                (Collect.q.collected_ended <= date) &
                                (Collect.q.collected_ended != None) &
                                (Hashtag.q.location == WoeidObject.id), 
                                join=LEFTJOINOn(None, Collect,Hashtag.q.collect == Collect.q.id)
                        )])
                
            #n = len(all_tags)

            statuses = list(set(all_tags))
            statuses = list(map(lambda status: status.replace('\n', ' '), statuses))
            statuses = list(map(lambda status: p.clean(status), statuses))
            statuses = list(map(lambda status: status.lower(), statuses))
            to_drop = string.punctuation
            to_drop = to_drop.replace('$', '').replace("'", '')
            for punct in to_drop:
                statuses = list(map(lambda status: status.replace(punct, ' '), statuses))        
            status_all = ' '.join(statuses)
            status_all = status_all.replace(" '", ' ')
            status_all = ' ' + status_all + ' '
            status_all = status_all.replace(' i ', ' I ')

            wordcloud = WordCloud(
                width = 2048,
                height = 2048,
                #max_words=20000, 
                background_color ='white', 
                min_font_size = 5
            ).generate(status_all)

            plt.figure(figsize = (10, 10), facecolor = None) 
            plt.imshow(wordcloud) 
            plt.axis("off") 
            plt.tight_layout(pad = 2) 
            plt.savefig(file_name)
            logging.info(f'{color.GREEN}[OK] Wordcloud of {WoeidObject.country} saved in \'{file_name}\' {color.END} ')

        except Exception as ae:
                logging.error(f'{color.RED}It is not possiblie get data from {WoeidObject.country}.{color.END}')
                logging.debug(ae)
    