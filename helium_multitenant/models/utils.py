from xml.etree.ElementTree import Element, tostring
import datetime
import random
import logging
import json

_logger = logging.getLogger(__name__)


def console_log(data):
    _logger.info(data)
    return