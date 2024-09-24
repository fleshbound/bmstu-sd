import logging
import os

def set_logger():
    LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
    LOGFILE = os.environ.get('LOGFILE', 'app.log')
    logging.basicConfig(filename=LOGFILE,
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s [%(levelname)s] %(message)s',
                        datefmt='%H:%M:%S',
                        level=LOGLEVEL)
