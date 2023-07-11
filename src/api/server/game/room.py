from flask_sock import Sock

from src.database.collections.rooms.utilities import RoomsDBUtils

class Room:
    def __init__(self, sock: Sock) -> None:
        self.sock = sock
        self.ROOM_ID = RoomsDBUtils.generate_unique_id()
        sock.route(f'/room/{self.ROOM_ID}')(self.handle) # TODO: Idk if this works 👍

    def handle(self, ws) -> None:
        print(type(ws))
        while True:
            data = ws.recv()
            print(data)
