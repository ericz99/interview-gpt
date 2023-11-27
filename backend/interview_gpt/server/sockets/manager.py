import socketio
from typing import List

from .namespaces.session import SessionNamespace

class SocketManager:
    def __init__(self, origins: List[str]) -> None:
        self.server = socketio.AsyncServer(
            cors_allowed_origins=origins,
            async_mode="asgi",
            logger=True,
        )
        self.app = socketio.ASGIApp(self.server)

    @property
    def on(self):
        return self.server.on
    
    @property
    def send(self):
        return self.server.send
    
    @property
    def emit(self):
        return self.server.emit
    
    def mount_to(self, path: str, app):
        app.mount(path, self.app)

    def register_ns(self, ns):
        self.server.register_namespace(ns)

socket_manager = SocketManager(["*", "http://localhost:3000"])
socket_manager.register_ns(ns=SessionNamespace('/session'))