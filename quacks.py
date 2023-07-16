from flask import Flask, request, g

from src.database.connection import QuacksDatabase
from src.api.server import WebSocketServer
from src.api.server.api.rooms import rooms


class Quacks:
    def __init__(self, app: Flask) -> None:
        """
            Initialize the database and register all required blueprints on the given app.
        """
        self.app = app
        self.__init_database()
        self.__init_websocket()
        self.__init_blueprints()

        self.app.before_request(self.__before_request)

    def __init_websocket(self) -> None:
        ws = WebSocketServer(self.app)
        ws.setup_websocket()

    def __init_database(self) -> None:
        self.db = QuacksDatabase()

    def __init_blueprints(self) -> None:
        self.app.register_blueprint(rooms)

    def __before_request(self):
        if request.method in ('POST', 'DELETE', 'PATCH'):
            try:
                g.data = request.get_json()
            except:
                g.data = {}


