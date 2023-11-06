import whisper
import torch
from queue import Queue
from dataclasses import dataclass
import asyncio
import os

@dataclass
class Transcriber():
    def __init__(self, model: str) -> None:
        self.queue = Queue()
        self.model = model
        self.output_path = './output'

    def load_all_audio(self):
        # grab all files in the output
        files = [f for f in os.listdir(self.output_path) if os.path.isfile(os.path.join(self.output_path, f)) and f.endswith('.wav')]
        # store them in a queue
        for file in files:
            self.queue.put(file)

    async def transcribe(self, f):
        # load english model only
        model = whisper.load_model(f'{self.model}.en')
        result = model.transcribe(f, fp16=torch.cuda.is_available())
        print(result)

        with open('transcription.txt', 'a') as f:
            f.write(f'{result["text"]} \n')

        await asyncio.sleep(0.25)

        print('done')