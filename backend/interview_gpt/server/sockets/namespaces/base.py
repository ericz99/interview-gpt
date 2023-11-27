import socketio
from loguru import logger
import asyncio

from interview_gpt.core.recorder import recorder

class BaseSocketNamespace(socketio.AsyncNamespace):
    def __init__(self, namespace=None):
        super().__init__(namespace)

    async def on_connect(self, sid, environ):
        logger.success(f'User connected {sid}')
        await self.setup()


    async def setup(self):
        logger.debug('Running initial setup!')

        async def run():
            stream = recorder.on_record_system()

            try:
                async for data in stream:
                    await self.emit('incoming data', data)
            except asyncio.CancelledError:
                logger.debug('Stream cancelled!')
                pass

        asyncio.create_task(run())

    def on_disconnect(self, sid):
        logger.warning(f'User disconnected {sid}')
