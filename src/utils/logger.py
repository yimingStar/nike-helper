import logging, logging.handlers
import os
import datetime
import sys

logger = logging.getLogger(__name__)

LOGGER_FORMAT = '%(asctime)s|%(levelname)-4s|[%(filename)s][%(funcName)s]| %(message)s'
formatter = logging.Formatter(LOGGER_FORMAT)

dir_path = os.getenv('LOG_PATH', None)
if dir_path is None:
    dir_path = './log/'
if not os.path.isdir(dir_path):
    os.makedirs(dir_path)
path = dir_path + '%s.log' % ('register')
file_handler = logging.handlers.TimedRotatingFileHandler(
    filename=path,
    when="midnight",
    interval=1,
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)