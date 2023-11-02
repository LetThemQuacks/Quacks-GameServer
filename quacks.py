from flask import Flask, request, g

from src.database.connection import QuacksDatabase
from src.api.server import WebSocketServer
from src.api.server.game.room import RoomServer
from src.api.plugins.controller import PluginController
from core import logging

import time

class Quacks:
    def __init__(self, app: Flask) -> None:
        """
            Initialize the database and register all required blueprints on the given app.
        """
        self.app = app
        self.init_time = time.time()

        self.__init_database()
        self.__init_websocket()
        
        self.__restore_rooms()

        self.__init_plugins()

        self.app.before_request(self.__before_request)

        self.app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 25}
        self.end_time = time.time()
        self.quacks_setup_time = self.end_time - self.init_time
        logging.info(f'[yellow bold]Quacks[/] is [green italic]ready![/] ( took {round(self.quacks_setup_time, 3)}s )')

    def __init_plugins(self) -> None:
        self.plugin_controller = PluginController()
        self.plugin_controller.load_plugins()

    def __init_websocket(self) -> None:
        ws = WebSocketServer(self.app)
        ws.setup_websocket()

    def __init_database(self) -> None:
        self.db = QuacksDatabase()

    def __restore_rooms(self) -> None:
        for room in self.db.rooms.list_rooms():
            room_data = self.db.rooms._setup_room_data(
                room['custom_id'], room['name'],
                room.get('password'), room.get('max_joins'),
                room.get('chat'),
                is_password_hash = True
            )

            WebSocketServer.rooms_instances[room['custom_id']] = RoomServer(
                WebSocketServer.INSTANCE, 
                room_data=room_data
            )

            logging.info(f'Restored Room [blue]->[/] id: [cyan][i]{room["custom_id"]}[/][/] name: [green][i]{room["name"]}[/][/]')



    def __before_request(self) -> None:
        if request.method in ('POST', 'DELETE', 'PATCH'):
            try:
                g.data = request.get_json()
            except:
                g.data = {}


