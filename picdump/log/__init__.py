
import sys
import logging
import logging.handlers
import picdump.utils

APP_NAME = 'picdump'


applogger = logging.getLogger(APP_NAME)

is_initialized = False


def init_logger(logfile="picdump.log", level=logging.INFO):
    global is_initialized
    if is_initialized:
        logging.getLogger('').warn('Logger Re-initialized!!')
        return
    logfilepath = picdump.utils.app_path(logfile)
    filehandler = logging.handlers.RotatingFileHandler(logfilepath, maxBytes=10240, backupCount=5)
    filehandler.setFormatter(logging.Formatter('%(asctime)s %(name)-24s %(levelname)-8s %(message)s'))
    consolehandler = logging.StreamHandler(sys.stdout)
    consolehandler.setFormatter(logging.Formatter('%(name)-24s %(levelname)-8s %(message)s'))
    applogger.addHandler(filehandler)
    applogger.addHandler(consolehandler)
    applogger.setLevel(level)
    is_initialized = True


def get_logger(name):
    return logging.getLogger('{}.{}'.format(APP_NAME, name))

