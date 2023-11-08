from cuid2 import Cuid
from dataclasses import dataclass

CUID_GENERATOR: Cuid = Cuid(length=10)

@dataclass
class Session:
    _sid: Cuid.generate()