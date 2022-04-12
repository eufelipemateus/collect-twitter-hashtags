import argparse
import logging
import schedule
import time
import os

from utils.console import color
from collect_hashtag import collect_hashtag
from migration.migration import migration 

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
    parser.add_argument('-c','--collect-hashtags', action='store_true', help="Collect hashtags from twitter. ")
  
    args = parser.parse_args() 

    if args.log_level:
        try:
            #logging.basicConfig(level=args.log_level)
            logging.basicConfig(filename=f'{os.path.splitext(os.path.basename(__file__))[0]}.log', encoding='utf-8',level=args.log_level)
        except ValueError:
            logging.error(f"{color.RED}Invalid log level: {args.log_level}{color.END}")
            exit(1)

    if args.migration: 
        try:
            migration()
            print(f"{color.GREEN}Script Finalizado com sucesso.{color.END}")
            exit()
        except Exception as e:
            logging.critical(f'{color.RED}Não foi possivel concluir a migração das tabelas.\n {e} {color.END}')
    
    if args.collect_hashtags:
        collect_hashtag()
        exit()
    if args.run_job:
        schedule.every(1).hours.do(collect_hashtag)
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    main()