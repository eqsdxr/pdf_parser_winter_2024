import logging
from logging.handlers import RotatingFileHandler

from pdf_parser.config import BASE_DIR

def setup_logger():
    logger = logging.getLogger('AppLogger')
    logger.setLevel(logging.DEBUG)
    
    # Create handlers (stream and file handlers)
    stream_handler = logging.StreamHandler()
    log_path = BASE_DIR / 'logs' / 'app.log'

    file_handler = RotatingFileHandler(
        log_path, 
        mode='a', 
        maxBytes=5*1024*1024, 
        backupCount=2, 
        encoding=None, 
        delay=0
    )

    # Set the logging level for each handler
    stream_handler.setLevel(logging.WARNING)
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()