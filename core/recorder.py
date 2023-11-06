import soundfile as sf
import soundcard as sc
import asyncio
from dataclasses import dataclass
from transcribe import Transcriber

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
        self.trans = Transcriber('base')

    async def on_record_system(self, duration):
        print('Recording...')

        with sc.get_microphone(id=(str(sc.default_speaker().name)), include_loopback=True).recorder(samplerate=RecorderConstant.RATE, channels=RecorderConstant.CHANNELS) as mic:
            while self._start_chuck < self._end_chuck:
                try:
                    print(f'Start Recording... Chuck: {self._start_chuck}')
                    # record audio with loopback from default speaker
                    data = mic.record(numframes=int(RecorderConstant.RATE * duration))
                    # writing to output wav, change data=data[:, 0] -> data=data if you want multiple channels, (recommended keeping multi, sound better)
                    file = f'./output/{RecorderConstant.OUTPUT_WAV}-c{self._start_chuck}.wav'
                    sf.write(file=file, samplerate=RecorderConstant.RATE, data=data)
                    print(f'Finished Recording... Chuck: {self._start_chuck}')
                    await asyncio.create_task(self.trans.transcribe(file))
                    self._start_chuck += 1
                    await asyncio.sleep(0.25)
                except KeyboardInterrupt:
                    print('Exiting...')
                    break
