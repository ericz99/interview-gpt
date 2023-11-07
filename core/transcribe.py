import whisper
import torch
from queue import Queue
from dataclasses import dataclass
import asyncio
import os
import re
from agent.chat import ChatAgent
from prompt.message import Message

@dataclass
class Transcriber():
    def __init__(self, model: str) -> None:
        self.agent = ChatAgent()
        self.queue = Queue()
        self.model = model
        self.output_path = './output'
        self._result_text = ''

    def load_all_audio(self):
        # grab all files in the output
        files = [f for f in os.listdir(self.output_path) if os.path.isfile(os.path.join(self.output_path, f)) and f.endswith('.wav')]
        # store them in a queue
        for file in files:
            self.queue.put(file)

    async def fix_transcript(self):
        # create new messages to be consumed
        message = Message(
            f'''
            Please fix this transcript, but try not to change any wording:

            {self._result_text}
            ''',
            role="user",
            name=None
        )

        # ask agent
        resp = await self.agent.ask(message)
        
        if resp is not None:
            content = resp.choices[0].message.content

            # update transcript, for more readible content
            with open('transcription.txt', 'w') as f:
                f.write(content)

    async def is_question(self, data):
        # create new messages to be consumed
        message = Message(
            f'''
            Based on this text can you confirm if its a question?:

            Text: {data}.

            Please only return response as an valid Python JSON object and nothing else.

            Example Response: {{ is_question: true }}
            ''',
            role="user",
            name=None
        )

        # ask agent
        resp = await self.agent.ask(message)

        if resp is not None:
            content = resp.choices[0].message.content
            matches = re.search(r'"is_question":\s*(\w+)', content)

            if matches:
                is_quest = matches.group(1)  # Extracting the value of "is_question"
                result = {"is_question": is_quest}
                return result
            
        return None
    
    async def answer(self, data):
        message = Message(
            f'''
                Given the following question, please answer to the best of your ability:

                Question: {data}
            ''',
            role="user",
            name=None
        )

        # ask agent
        resp = await self.agent.ask(message)

        if resp is not None:
            content = resp.choices[0].message.content
            print(content)

    async def transcribe(self, f):
        # load english model only
        model = whisper.load_model(f'{self.model}.en')
        result = model.transcribe(f, fp16=torch.cuda.is_available())
        text = result['text']
        self._result_text += f'{text} \n'
        print(f'{text} \n')

        with open('transcription.txt', 'a') as f:
            f.write(f'{text} \n')

        is_que = await self.is_question(text)

        if is_que:
            print('is question!!!')
            await self.answer(text)


        await asyncio.sleep(0.25)

        print('done')