import os
import logging
from datetime import datetime as d

from utils.console import color
import bar_chart_race as bcr
from utils.mysql import conn
from sqlobject.sqlbuilder import *
from model.Collects import Collect
from model.Hashtags import Hashtag
from model.Woeids import Woeid

from pandas import DataFrame

video_path = os.getenv("VIDEO_PATH")
date = d.now()
firstDayMonth = date.replace(day=1);

def chart_race():
    for WoeidObject in Woeid.select():

        try:
            logging.info(f'Genereting chart-race from  {Woeid.q.country}')

            file_name =  video_path + WoeidObject.code + date.strftime("-%Y-%m") + '.mp4'

            select = Select(
                items=[
                    "date_format(created, '%Y-%m-%d') as date",
                    'text',
                    'COUNT(text)'
                ],
                staticTables=['hashtags'],
                where=(
                    (Collect.q.collected_ended >= firstDayMonth) &
                    (Collect.q.collected_ended <= date) &
                    (Collect.q.collected_ended != None) &
                    (Hashtag.q.location == WoeidObject.id), 
                ),
                join=LEFTJOINOn(None, Collect,Hashtag.q.collect == Collect.q.id),
                groupBy='text,date_format(created, \'%Y-%m-%d\'), location_id',
                orderBy='date ASC'
            ) 
            query = conn.sqlrepr(select)
            rows = conn.queryAll(query)

            if not rows:
                logging.error(f'{color.RED} Don\'t have any data from {WoeidObject.country}. {color.END}')
                continue


            df = DataFrame(rows, columns=['date', 'text', 'total']).pivot(index='date', columns='text', values='total').fillna(0)
            df_values, df_ranks = bcr.prepare_wide_data(
                    df,
                    steps_per_period=20,
                    orientation='h',
                    interpolate_period=True,
                    sort='desc'
            )
            df_values.head(16)

            
            bcr.bar_chart_race(
                df_ranks,
                filename=file_name, 
                period_length=1000,
                fixed_max=True,
                fixed_order=False,
                filter_column_colors=True,
                n_bars=10,
                figsize=(10, 5),
                period_fmt='Day {x}',
                title='Top Trends Peer Day - TrendsCads.com'
            )
            logging.info(f'{color.GREEN}[OK] chart-race of {WoeidObject.country} saved in \'{file_name}\'. {color.END}')

        except Exception as ae:
            logging.error(f'{color.RED} Error while trying generate chart-race to {WoeidObject.country}. {color.END}')
            logging.debug(ae)


