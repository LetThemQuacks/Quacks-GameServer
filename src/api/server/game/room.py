from flask_sock import Sock

from src.database.collections.rooms.rooms import RoomsCollection
from src.api.server.types.client import Packet

class RoomServer:
    """
        In-game WebSocket Server for a single Room.
    """

    def __init__(self, server_instance, room_data: dict) -> None:
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
        self.sock: Sock = server_instance.sock
        self.server_instance = server_instance
        self.ROOM_ID = room_data['custom_id']
        self.ROOM_DATA = room_data

        self.chat = self.ROOM_DATA.get('chat')

        self.online_users: list = []

    def broadcast(self, data: Packet, exceptions: tuple = tuple()):
        for client in self.online_users:
            if client in exceptions: continue
            client.send(data)

    def user_join(self, client):
        self.broadcast({'type': 'user_join', 'data': {
            'username': client.username,
            'id': client.user_id,
            'skin': client.skin
        }}, (client,))
        self.online_users.append(client)
        client.CURRENT_ROOM = self

    def user_left(self, client):
        self.online_users.remove(client)
        self.broadcast({'type': 'user_left', 'data': {
            'id': client.user_id,
        }}, (client,))

        # If there's no chat the room is ephemeral
        if not self.chat and len(self.online_users) == 0:
            self.delete()

    def user_movement(self, client):
        self.broadcast({'type': 'move', 'data': {
            'id': client.user_id,
            'state': client.public_physics_state
        }})

    def delete(self): # I hate circular import errors
        self.server_instance.rooms_instances.pop(self.ROOM_ID) 
        RoomsCollection.INSTANCE.delete_room(self.ROOM_ID)

        self.broadcast({
            'type': 'kick',
            'data': {
                'reason': 'ROOM_DELETED'
            }
        })

    def online_dict(self, exclude = None):
        return [user.jsonify() for user in self.online_users if user != exclude]

    def __iter__(self):
        self.clients_iteration_index = 0
        return self

    def __next__(self):
        if self.clients_iteration_index >= len(self.online_users):
            raise StopIteration

        client = self.online_users[self.clients_iteration_index]
        self.clients_iteration_index += 1
        return client

    def __getitem__(self, key):
        for client in self:
            if client.user_id == key:
                return client
        raise KeyError(key)
