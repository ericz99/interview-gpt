import soundfile as sf
import soundcard as sc
import asyncio
from dataclasses import dataclass
from transcribe import Transcriber
import numpy as np
from queue import Queue
import os
from datetime import datetime, timedelta

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
        self._storage = []
        self.trans = Transcriber('base')
        self.queue = Queue()

    async def save_to_queue(self, data):
        self.queue.put(data)

    async def save_to_file(self, data, is_session = False):
        print('Saving to file')

        _path = os.path.abspath(os.path.join(os.path.__file__, '..', '..', 'output'))
        
        if is_session:
            # writing to output wav, change data=data[:, 0] -> data=data if you want multiple channels, (recommended keeping multi, sound better)
            file = f'{_path}/{RecorderConstant.OUTPUT_WAV}-session.wav'
        else:
            # writing to output wav, change data=data[:, 0] -> data=data if you want multiple channels, (recommended keeping multi, sound better)
            file = f'{_path}/{RecorderConstant.OUTPUT_WAV}-c{self._start_chuck}.wav'

        sf.write(file=file, samplerate=RecorderConstant.RATE, data=data)
        print(f'Finished Recording... Chuck: {self._start_chuck}')
        await asyncio.create_task(self.trans.transcribe(file))
        self._start_chuck += 1
        await asyncio.sleep(0.25)
        # os.remove(file)

    async def on_record_session(self, data):
        try:
            self._storage.append(data)
        except KeyboardInterrupt:
            if not len(self._storage) == 0:
                res_data = np.concatenate(self._storage, dtype='float64')
                await self.save_to_file(res_data, True)
                print(f'Finished Processing Recording Session...')

    async def on_record_system(self):
        '''
        on_record_system:
        method to record system device, such as speaker.
        After certain time if no sound is being produced in the speaker,
        it will save and download frames
        '''
        print('Recording...')
        minimum_threshold = 0.000001
        duration_threshold = 5
        has_spoken = False

        with sc.get_microphone(id=(str(sc.default_speaker().name)), include_loopback=True).recorder(samplerate=RecorderConstant.RATE, channels=RecorderConstant.CHANNELS) as mic:
            while True:
                try:
                    data = mic.record(numframes=None)
                    rms = np.mean(np.square(data))
                    now = datetime.now()
                    end_time = now + timedelta(seconds=duration_threshold)

                    if rms > minimum_threshold:
                        await self.save_to_queue(data)
                        await self.on_record_session(data)
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
                                res_data = np.concatenate(res, dtype='float64')
                                await self.save_to_file(res_data)
                                await asyncio.create_task(self.trans.fix_transcript())

                        has_spoken = False

                    await asyncio.sleep(0)
                except KeyboardInterrupt:
                    print('Exiting...')
                    break
