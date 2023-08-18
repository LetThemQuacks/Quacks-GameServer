from flask_sock import Sock
from .client import WebSocketClient

class WebSocketServer:
    INSTANCE: 'WebSocketServer'
    rooms_instances = {} # id: instance

    def __init__(self, app) -> None:
        if getattr(WebSocketServer, 'INSTANCE', None):
            raise RuntimeError('WebsocketServer is a singletone object.')
        WebSocketServer.INSTANCE = self
        self.app = app

    def setup_websocket(self) -> None:
        """
            Setups the websocket server for the specified app.
        """
        self.sock = Sock(self.app)
        self.sock.route('/room')(WebSocketClient)

