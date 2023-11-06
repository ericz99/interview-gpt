import os
import openai
from base import BaseAIModel
from utils import get_only_content_token_length, get_token_model_limit

# set up configuration
openai.organization = "YOUR_ORG"
openai.api_key = os.getenv('OPENAI_API_KEY')

class OpenAIModel(BaseAIModel):
    def __init__(self, model: str = 'gpt-3.5-turbo-0613') -> None:
        super().__init__()
        self.model = model
        self.ai = openai

    '''
    Generate embedding vector
    '''
    async def generate_embedding(self, input: str):
        response = self.ai.Embedding.create(
            input=input,
            model="text-embedding-ada-002"
        )
        
        embeddings = response['data'][0]['embedding']
        return embeddings

    '''
    Generate LLM call once
    '''
    async def generate(self, messages):
        num_token_in_ctx = get_only_content_token_length(messages, self.model)
        win_size = 15 * len(messages)
        num_token_in_ctx += win_size
        model_token_limit = get_token_model_limit(self.model)
        completion_token = model_token_limit - num_token_in_ctx

        response = self.ai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            max_tokens=completion_token,
            n=1,
            top_p=1.0,
            temperature=0.4,
            presence_penalty=0.0,
            frequency_penalty=0.0,
            logit_bias={},
            user="",
        )

        return response