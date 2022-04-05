import argparse
import logging
from utils.console import color
from collect_hashtag import collect_hashtag
from migration.migration import migration 
  
def main(): 
  
    parser = argparse.ArgumentParser(
        prog='thts',
        usage='%(prog)s [options]',
        description ='This programa collect data from twitter and sabe on database.'
    ) 
  
    parser.add_argument('-m','--migration', action='store_true',  help ='Create and seed all tables.') 
    parser.add_argument('-l', '--log-level', default='WARNING',
                                  help='Set log level')
    parser.add_argument('-c','--collect', action='store_true', help="Collect hashtags from twitter. ")
  
    args = parser.parse_args() 

    if args.log_level:

        try:
            logging.basicConfig(level=args.log_level)
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
    
    if args.collect:
        collect_hashtag()
        exit()


if __name__ == "__main__":
    main()