import soundfile as sf
import soundcard as sc
import asyncio
from dataclasses import dataclass
import numpy as np
from queue import Queue
import os
from datetime import datetime, timedelta
from loguru import logger
from typing import Optional

from interview_gpt.core.transcribe import Transcriber


class RecorderConstant:
    RATE = 44100
    CHANNELS = 2
    OUTPUT_WAV = "sample-output"
    CHUNK = 1024


@dataclass
class Recorder:
    def __init__(self, path: Optional[str] = None) -> None:
        self.path = path
        self._start_chuck: int = 0
        self._end_chuck: int = 10
        self._max_second: int = 10
        self._storage = []
        self.trans = Transcriber("base")
        self.queue = Queue()
        self.should_record_session = False
        self.is_active = False

    def set_active(self, bool):
        self.is_active = bool

    def set_record_session(self, bool):
        self.should_record_session = bool

    def set_path(self, path):
        self.path = path

    async def save_to_queue(self, data):
        self.queue.put(data)

    async def save_to_file(self, data, is_session=False):
        logger.debug("Saving to file")
        _path = os.path.abspath(os.path.join(os.curdir, "..", "..", '..', "output"))

        if is_session:
            # writing to output wav, change data=data[:, 0] -> data=data if you want multiple channels, (recommended keeping multi, sound better)
            file = f"{_path}\\{RecorderConstant.OUTPUT_WAV}-session.wav"
        else:
            # writing to output wav, change data=data[:, 0] -> data=data if you want multiple channels, (recommended keeping multi, sound better)
            file = f"{_path}\\{RecorderConstant.OUTPUT_WAV}-c{self._start_chuck}.wav"

        sf.write(file=file, samplerate=RecorderConstant.RATE, data=data)
        print(f"Finished Recording... Chuck: {self._start_chuck}")
        res = await asyncio.create_task(self.trans.transcribe(file))
        self._start_chuck += 1
        await asyncio.sleep(0)
        os.remove(file)
        return res

    async def process_recording(self):
        if not len(self._storage) == 0:
            res_data = np.concatenate(self._storage, dtype="float64")
            await self.save_to_file(res_data, True)
            logger.debug("Finished Processing Recording Session...")

    async def on_record_system(self):
        """
        on_record_system:
        method to record system device, such as speaker.
        After certain time if no sound is being produced in the speaker,
        it will save and download frames
        """
        logger.debug("Recording...")
        minimum_threshold = 0.0000001
        duration_threshold = 2
        has_spoken = False

        with sc.get_microphone(
            id=(str(sc.default_speaker().name)), include_loopback=True
        ).recorder(
            samplerate=RecorderConstant.RATE, channels=RecorderConstant.CHANNELS
        ) as mic:
            while True:
                try:
                    data = mic.record(numframes=None)
                    rms = np.mean(np.square(data))
                    now = datetime.now()
                    end_time = now + timedelta(seconds=duration_threshold)

                    if rms > minimum_threshold:
                        await self.save_to_queue(data)
                        
                        if self.should_record_session:
                            await self._storage.append(data)

                        has_spoken = True
                    else:
                        res = []

                        # give a small buffer time
                        while has_spoken and datetime.now() < end_time:
                            data = mic.record(numframes=None)
                            rms = np.mean(np.square(data))

                            if rms > minimum_threshold:
                                has_spoken = False

                        # check if buffer had passed
                        if has_spoken and datetime.now() > end_time:
                            while not self.queue.empty():
                                frame = self.queue.get()
                                res.append(frame)

                            if not len(res) == 0:
                                res_data = np.concatenate(res, dtype="float64")
                                output = await self.save_to_file(res_data)

                                if not output:
                                    continue

                                yield output
                                # await asyncio.create_task(self.trans.ai.fix_transcript(output))

                        has_spoken = False

                    await asyncio.sleep(0)
                except KeyboardInterrupt:
                    logger.error("Exiting...")
                    break


recorder = Recorder()
