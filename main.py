import argparse
import logging
import schedule
import threading
import time
import os

from utils.console import color
from collect_hashtag import collect_hashtag
from cloudwords import cloud_words
from chartrace import chart_race
from migration.migration import migration 


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

def main(): 
  
    parser = argparse.ArgumentParser(
        prog='thts',
        usage='%(prog)s [options]',
        description ='This programa collect data from twitter and seed on database.'
    ) 
  
    parser.add_argument('-run', '--run-job', action='store_true', help='Run cron job.')
    parser.add_argument('-m','--migration', action='store_true',  help ='Migrate database  Create and seed all tables.') 
    parser.add_argument('-l', '--log-level', default='WARNING',
                                  help='Set log level')

    parser.add_argument('-lf', '--log-file',help='Set log file to save logs')
    parser.add_argument('-c','--collect-hashtags', action='store_true', help="Collect hashtags from twitter. ")
    parser.add_argument('-cw','--cloud-words', action='store_true', help="This option is for generate cloud word.")
    parser.add_argument('-cr','--chart-race', action='store_true', help="This option will generate video with chart race to trends words.")

    args = parser.parse_args() 

    if args.log_level:
        try:
            logging.basicConfig(level=args.log_level)
            #logging.basicConfig(filename=f'{os.path.splitext(os.path.basename(__file__))[0]}.log', encoding='utf-8',level=args.log_level)
        except ValueError:
            logging.error(f"{color.RED}Invalid log level: {args.log_level}{color.END}")
            exit(1)


    if args.log_file:
        try:
            logging.basicConfig(filename=f'{args.log_file}.log', encoding='utf-8',level=args.log_level)
        except ValueError:
            logging.error(f"{color.RED}Invalid log level: {args.log_level}{color.END}")
            exit(1)

    if args.migration: 
        try:
            if(migration()):
                print(f"{color.GREEN}Script Finalizado com sucesso.{color.END}")
                exit()
        except Exception as e:
            logging.critical(f'{color.RED}Não foi possivel concluir a migração das tabelas.\n {e} {color.END}')
    
    if args.collect_hashtags:
        collect_hashtag()
        exit()

    if args.cloud_words:
        cloud_words()
        exit()

    if args.chart_race:
        chart_race()
        exit()

    if args.run_job:
        
        schedule.every().hour.do(collect_hashtag)
        schedule.every(6).hours.do(run_threaded, cloud_words)
        schedule.every().day.at("02:30").do(run_threaded, chart_race)

        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    main()