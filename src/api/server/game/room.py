from flask_sock import Sock

from src.database.collections.rooms.utilities import RoomsDBUtils

class RoomServer:
    """
        In-game WebSocket Server for a single Room.
    """

    def __init__(self, sock: Sock, room_id: str, room_data: dict) -> None:
        """
            Create a websocket route at /room/<room_id>/ for the specified room.
            
            :Parameters:
                - `sock`: Main WebSocket Server instance.
                - `room_id`: Unique room ID.
                - `room_data`: A dict containing all the room informations.
                ```json
                {
                    "name": "test",
                    "pwd": "<hash ...>",
                    "max_join": 5
                }
                ```

        """
        self.sock = sock
        self.ROOM_ID = room_id[:-1]
        self.ROOM_DATA = room_data

    def handle_packet(self, packet) -> None:
        print(packet)
