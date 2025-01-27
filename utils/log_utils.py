import os
from loguru import logger
from configs.constants import LOG_DIR

logger.add(os.path.join(LOG_DIR, 'log.log'), format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}', level='DEBUG')
