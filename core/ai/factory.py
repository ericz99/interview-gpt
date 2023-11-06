from _openai import OpenAIModel

class AIFactory():
    @classmethod
    def create(self, llm, model_type):
        if llm is 'openai':
            return OpenAIModel(model_type)