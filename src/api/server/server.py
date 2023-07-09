from flask_sock import Sock

class WebsocketServer:
    INSTANCE = None

    def __new__(cls) -> object:
        if not cls.INSTANCE:
            cls.INSTANCE = super(WebsocketServer, cls).__new__(cls)
        return cls.INSTANCE

    def __init__(self, app) -> None:
        self.app = app

    def setup_websocket(self) -> None:
        """
            Setups the websocket server for the specified app.
        """
        self.sock = Sock(self.app)


