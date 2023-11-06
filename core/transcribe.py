import whisper
import torch
from queue import Queue
from dataclasses import dataclass
import asyncio
import os
from agent.chat import ChatAgent
from prompt.message import Message

@dataclass
class Transcriber():
    def __init__(self, model: str) -> None:
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
            Please fix this transcript, like indentation, grammar, and etc:

            {self._result_text}
            ''',
            role="user",
            name=None
        )

        agent = ChatAgent()
        resp = await agent.ask(message)
        
        if resp is not None:
            content = resp.choices[0].message.content

            # update transcript, for more readible content
            with open('transcription.txt', 'w') as f:
                f.write(content)


    async def transcribe(self, f):
        # load english model only
        model = whisper.load_model(f'{self.model}.en')
        result = model.transcribe(f, fp16=torch.cuda.is_available())
        self._result_text += f'{result["text"]} \n'
        print(f'{result["text"]} \n')

        with open('transcription.txt', 'a') as f:
            f.write(f'{result["text"]} \n')

        await asyncio.sleep(0.25)

        print('done')