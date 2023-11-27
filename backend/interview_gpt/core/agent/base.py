from abc import ABC, abstractmethod
from dataclasses import dataclass
from cuid2 import Cuid

from interview_gpt.core.utils import text_to_chuck
from interview_gpt.core.ai.factory import AIFactory
from interview_gpt.core.db.pinecone import PineConeEmbed

CUID_GENERATOR: Cuid = Cuid(length=10)


@dataclass
class BaseAgent(ABC):
    backend = AIFactory().create("openai", "gpt-3.5-turbo-0613")
    db = PineConeEmbed(api_key=None)

    async def add_document(self, doc):
        try:
            # convert text and split into chucks
            chucks = text_to_chuck(doc, 2000)

            for chuck in chucks:
                embedding = await self.backend.generate_embedding(chuck)
                self.db.upsert(
                    {
                        # change to dynamic value
                        "vectors": [
                            {
                                "id": f"resume-{CUID_GENERATOR.generate()}",
                                "values": embedding,
                                "metadata": {"is_resume": True, "is_document": True},
                            }
                        ]
                    }
                )

        except Exception as e:
            print(e)

    @abstractmethod
    async def ask(self, message):
        pass
