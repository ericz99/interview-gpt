from dataclasses import dataclass
from typing import Optional
import json

@dataclass
class Message:
    content: str
    role: str
    name: Optional[str]

class MessageEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message):
            return obj.__dict__
        return super(MessageEncoder, self).default(obj)