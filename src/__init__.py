import logging
from dataclasses import dataclass

logging.basicConfig(level="DEBUG")


@dataclass
class Sex:
    name: str
    gender: str


#
# try:
#     2 / 0
# except ZeroDivisionError as exc:
#     logging.debug(msg='s', exc_info=exc)
# FORMAT = '%(event)-8s'
# logging.basicConfig(format=FORMAT)
# logging.debug('s', extra={'event': Sex(name='dick', gender='hitler')})
