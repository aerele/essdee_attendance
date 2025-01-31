import logging
from logging.handlers import RotatingFileHandler
import frappe


LOG_FILENAME = '../logs/hrms_log_handler.log'
logger = None
module_name = __name__

def get_module_logger():
    global logger
    if logger is not None:
        return logger

    formatter = logging.Formatter('[%(levelname)s] %(asctime)s | %(pathname)s:%(message)s\n')

    handler = RotatingFileHandler(
        LOG_FILENAME, maxBytes=100000, backupCount=20)
    handler.setFormatter(formatter)

    logger = logging.getLogger(module_name)
    logger.setLevel(frappe.log_level or logging.DEBUG)
    logger.addHandler(handler)
    logger.propagate = False

    return logger