import soundfile as sf
import soundcard as sc
import asyncio
from dataclasses import dataclass
from transcribe import Transcriber
import numpy as np
from queue import Queue
import os

class RecorderConstant:
    RATE = 44100
    CHANNELS = 2
    OUTPUT_WAV = 'sample-output'
    CHUNK = 1024


@dataclass
class Recorder():
    def __init__(self, path: str) -> None:
        self.path = path
        self._start_chuck: int = 0
        self._end_chuck: int = 10
        self._max_second: int = 10
        self._storage = {}
        self.trans = Transcriber('base')
        self.queue = Queue()

    async def save_to_queue(self, data):
        self.queue.put(data)

    async def save_to_file(self, data):
        print('Saving to file')
        # writing to output wav, change data=data[:, 0] -> data=data if you want multiple channels, (recommended keeping multi, sound better)
        file = f'./output/{RecorderConstant.OUTPUT_WAV}-c{self._start_chuck}.wav'
        sf.write(file=file, samplerate=RecorderConstant.RATE, data=data)
        print(f'Finished Recording... Chuck: {self._start_chuck}')
        await asyncio.create_task(self.trans.transcribe(file))
        self._start_chuck += 1
        await asyncio.sleep(0.25)
        # os.remove(file)

    async def on_record_system(self):
        print('Recording...')

        with sc.get_microphone(id=(str(sc.default_speaker().name)), include_loopback=True).recorder(samplerate=RecorderConstant.RATE, channels=RecorderConstant.CHANNELS) as mic:
            while True:
                try:
                    data = mic.record(numframes=None)
                    is_empty_block = np.all(data == 0)

                    if not is_empty_block:
                        await self.save_to_queue(data)
                    else:
                        res = []

                        while not self.queue.empty():
                            print('Getting item in queue')
                            frame = self.queue.get()
                            res.append(frame)

                        if not len(res) == 0:
                            res_data = np.concatenate(res, dtype='float64')
                            # save to file
                            await self.save_to_file(res_data)
                        else:
                            print('nothing')

                    await asyncio.sleep(0)
                except KeyboardInterrupt:
                    print('Exiting...')
                    break
