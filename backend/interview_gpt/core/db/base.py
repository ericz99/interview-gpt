from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class BaseAIEmbedDB(ABC):
    api_key: Optional[str]

    @abstractmethod
    def upsert(self):
        pass

    @abstractmethod
    def query(self):
        pass
