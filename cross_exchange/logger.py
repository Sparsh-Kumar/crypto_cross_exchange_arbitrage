import os
import logging
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = 'cross_exchange', log_dir: str = 'logs') -> logging.Logger:
  logger = logging.getLogger(name)
  logger.setLevel(logging.DEBUG)
  
  if logger.handlers:
    return logger
  
  Path(log_dir).mkdir(parents=True, exist_ok=True)
  
  log_file = os.path.join(log_dir, f'{name}_{datetime.now().strftime("%Y%m%d")}.log')
  file_handler = RotatingFileHandler(
    log_file,
    maxBytes=10 * 1024 * 1024,
    backupCount=5,
    encoding='utf-8'
  )
  file_handler.setLevel(logging.DEBUG)
  file_formatter = logging.Formatter(
    '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
  )
  file_handler.setFormatter(file_formatter)
  logger.addHandler(file_handler)
  
  console_handler = logging.StreamHandler()
  console_handler.setLevel(logging.INFO)
  console_formatter = logging.Formatter(
    '%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
  )
  console_handler.setFormatter(console_formatter)
  logger.addHandler(console_handler)
  
  return logger

logger = setup_logger()

