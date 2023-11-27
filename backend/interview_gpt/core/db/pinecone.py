import pinecone
import os
from dataclasses import dataclass

from .base import BaseAIEmbedDB


@dataclass
class PineConeEmbed(BaseAIEmbedDB):
    index = pinecone.Index(os.getenv("PINECONE_INDEX"))

    def upsert(self, req, update=False):
        if not update:
            self.index.upsert(vectors=req.vectors)
        else:
            self.index.update(id=req.id, values=req.values, set_metadata=req.metadata)

    def query(self, req):
        if req.text:
            raise Exception("Pinecone does not support text.")

        resp = self.index.query(
            top_k=req.limit, id=req.id, include_metadata=True, include_values=True
        )

        query_matcher = {"matches": []}

        for res in resp:
            query_matcher["matches"].append(
                {"id": res.id, "score": res.score, "metadata": res.metadata}
            )

        return query_matcher
