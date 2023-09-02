
import logging,os
from datetime import datetime
from constants import VARIATIONS

def check_and_create_folder_log():
    if not os.path.exists(VARIATIONS.FOLDER_LOG) or not os.path.isdir(VARIATIONS.FOLDER_LOG):
        os.makedirs(VARIATIONS.FOLDER_LOG)
class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formaterror = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + formaterror + reset,
        logging.ERROR: red + formaterror + reset,
        logging.CRITICAL: bold_red + formaterror + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt,datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)
    
def loggerHelper(namepase):
    logger = logging.getLogger(namepase)
    logger.setLevel(logging.INFO)
    log_filename = f'{VARIATIONS.FOLDER_LOG}/log_{datetime.now().strftime("%Y-%m-%d")}.log'
    file_handler = logging.FileHandler(log_filename)
    formatter = logging.Formatter('[%(asctime)s] - [%(levelname)s] - [%(name)s] - [%(funcName)s] - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)

    ch = logging.StreamHandler()

    ch.setFormatter(CustomFormatter())

    logger.addHandler(ch)

    logger.addHandler(file_handler)
    return logger