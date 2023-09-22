from dataclasses import dataclass
from typing import Any


@dataclass
class ApplicationException(Exception):
    value: Any
