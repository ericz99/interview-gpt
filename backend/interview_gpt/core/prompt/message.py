from dataclasses import dataclass
from typing import Optional


@dataclass
class Message:
    content: str
    role: str
    name: Optional[str]
