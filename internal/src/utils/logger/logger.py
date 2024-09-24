import logging
import os

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.getLogger().setLevel(level=LOGLEVEL)
