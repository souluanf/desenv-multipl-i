import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler


def setup_logging():
    log_format = '%(asctime)s [%(threadName)s] [aula05] %(levelname)s %(name)s.%(funcName)s - %(message)s'
    logger = logging.getLogger("fastapi")
    logger.setLevel(logging.INFO)

    log_directory = 'logs'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(fmt=log_format))
    logger.addHandler(console_handler)

    # Filee handler
    file_handler = TimedRotatingFileHandler('logs/myapp.log', when='midnight', interval=1, backupCount=30,
                                            encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(fmt=log_format))
    logger.addHandler(file_handler)

    return logger
