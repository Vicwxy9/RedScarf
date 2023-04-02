import datetime
import logging
from logging.handlers import RotatingFileHandler
import threading

lock = threading.Lock()

def log(str:str, file_path:str="./logs/log.log", level:str='INFO', time_format:str='%Y-%m-%d %H:%M:%S', max_size:int=1024*1024, backup_count:int=5):
    datetime_object = datetime.datetime.now()
    datetime_str = datetime_object.strftime(time_format)
    handler = RotatingFileHandler(file_path, maxBytes=max_size, backupCount=backup_count)
    formatter = logging.Formatter(f'[{datetime_str} %(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(handler)
    if level == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    elif level == 'WARNING':
        logger.setLevel(logging.WARNING)
    elif level == 'ERROR':
        logger.setLevel(logging.ERROR)
    else:
        logger.setLevel(logging.INFO)
    with lock:
        logger.debug(str) if level == 'DEBUG' else logger.warning(str) if level == 'WARNING' else logger.error(str) if level == 'ERROR' else logger.info(str)
        print(f'[{datetime_str} {level}] {str}')