import logging
import datetime, platform
import logging.handlers

# _file_format = logging.Formatter(
#     fmt=f"%(levelname)s %(asctime)s (%(relativeCreated)d) \t %(pathname)s F%(funcName)s L%(lineno)s - %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
# )

rootdir = None
splitter = None
print("my plaform : ", platform.system())
if platform.os=='Windows':
    splitter = "\\"
    rootdir = ".\\logs"
else:
    rootdir = "./logs"
    splitter = "/"
    
# _file_format=f"%(levelname)s %(asctime)s (%(relativeCreated)d) \t %(pathname)s F%(funcName)s L%(lineno)s - %(message)s",
_file_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
# _log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"

def get_file_handler(name, format):
    file_handler = logging.handlers.TimedRotatingFileHandler(
        rootdir + splitter + name,
        when='D'
    )
    file_handler.suffix = format
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter(_file_format))
    return file_handler

def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_file_format))
    return stream_handler

def get_logger(name, log_fname, format="%Y%m%d%H%M"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler(log_fname,format))
    logger.addHandler(get_stream_handler())
    return logger