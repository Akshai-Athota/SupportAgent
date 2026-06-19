import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logging(level:str="INFO"):
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    ))
    root = logging.getLogger()
    root.handlers.clear()      
    root.addHandler(handler)
    root.setLevel(level)