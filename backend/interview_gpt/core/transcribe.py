import whisper
import torch
from queue import Queue
from dataclasses import dataclass
import os
from loguru import logger
from typing import Optional

from interview_gpt.core.agent.assistant import AssistantAgent


@dataclass
class Transcriber:
    def __init__(self, model: Optional[str] = "gpt-3.5-turbo-1106") -> None:
        self.ai = AssistantAgent()
        self.queue = Queue()
        self.model = model
        self.output_path = "./output"

    def set_model(self, model):
        self.model = model

    def load_all_audio(self):
        # grab all files in the output
        files = [
            f
            for f in os.listdir(self.output_path)
            if os.path.isfile(os.path.join(self.output_path, f)) and f.endswith(".wav")
        ]
        # store them in a queue
        for file in files:
            self.queue.put(file)

    async def transcribe(self, f):
        # load english model only
        model = whisper.load_model(f"{self.model}.en")
        result = model.transcribe(f, fp16=torch.cuda.is_available())
        text = result["text"]
        logger.debug(f"{text} \n")

        if len(text) == 0:
            return None

        with open("transcription.txt", "a") as f:
            f.write(f"{text} \n")

        is_que = await self.ai.is_question(text)
        ai_resp = None

        if is_que:
            ai_resp = await self.ai.answer(text)

        return {
            "transcript": text,
            "answer": ai_resp
        }


transcribe = Transcriber()
