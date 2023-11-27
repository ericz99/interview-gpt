from abc import ABC, abstractmethod


class BaseAIModel(ABC):
    @abstractmethod
    async def generate(self, messages):
        pass
