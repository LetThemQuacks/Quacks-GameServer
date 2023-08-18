from flask import Flask, request, g

from src.database.connection import QuacksDatabase
from src.api.server import WebSocketServer
from src.api.server.game.room import RoomServer
from src.api.server.api.rooms import rooms
from core import logging

import yaml

class Quacks:
    def __init__(self, app: Flask) -> None:
        """
            Initialize the database and register all required blueprints on the given app.
        """
        self.app = app

        self.__load_configs()

        self.__init_database()
        self.__init_websocket()
        self.__init_blueprints()
        
        self.__restore_rooms()

        self.app.before_request(self.__before_request)

        self.app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 25}
        logging.info('[yellow bold]Quacks[/] is [green italic]ready![/]')

    def __load_configs(self) -> None:
        with open('configs.yml', 'r', encoding='utf-8') as file:
            self.configs = yaml.safe_load_all(file)

    def __init_websocket(self) -> None:
        ws = WebSocketServer(self.app)
        ws.setup_websocket()

    def __init_database(self) -> None:
        self.db = QuacksDatabase()

    def __init_blueprints(self) -> None:
        self.app.register_blueprint(rooms)

    def __restore_rooms(self) -> None:
        for room in self.db.rooms.list_rooms():
            WebSocketServer.rooms_instances[room['custom_id']] = RoomServer(
                WebSocketServer.INSTANCE.sock,
                room_data=self.db.rooms._setup_room_data(
                    room['custom_id'],
                    room['name'],
                    room.get('password'),
                    room.get('max_joins')
                )
            )
            logging.info(f'Restored Room [blue]->[/] id: [cyan][i]{room["custom_id"]}[/][/] name: [green][i]{room["name"]}[/][/]')



    def __before_request(self) -> None:
        if request.method in ('POST', 'DELETE', 'PATCH'):
            try:
                g.data = request.get_json()
            except:
                g.data = {}


