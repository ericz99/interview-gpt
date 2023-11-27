import json
from loguru import logger

from .base import BaseSocketNamespace

class SessionNamespace(BaseSocketNamespace):
    def __init__(self, namespace=None):
        super().__init__(namespace)
        self.namespace = namespace

    async def on_session_created(self, sid, data):
        '''
        when new session has been created
        '''
        session = json.loads(data)

        print(data)

        if session['room_id']:
            await self.enter_room(room=session['room_id'], namespace=self.namespace)

    async def on_session_expired(self, sid, data):
        '''
        when session has been expire
        '''
        session = json.loads(data)

        print(data)

        if session['room_id']:
            await self.leave_room(room=session['room_id'], namespace=self.namespace)

    async def on_ping(self, sid, data):
        '''
        simple ping pong status
        '''
        print(sid)
        print(data)
        await self.emit('pong', 'hello world')