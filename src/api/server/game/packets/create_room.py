from .handler import PacketHandler, QuickFilters
from ...client import WebSocketClient
from ...server import WebSocketServer

from .....database.collections.rooms.rooms import RoomsCollection
from .....database.errors import RoomsErrors
from .....api.server.game.room import RoomServer

from core import logging
from json import dumps

import quacks
 
@PacketHandler.handle(packet_type='create_room', filters=[QuickFilters.any_null_value])
def create_room(client: WebSocketClient, data: dict) -> None:
    if not quacks.configs['room_creation']['allow']:
        return client.send(dumps({'type': 'error', 'data': {
            'from_packet_type': 'create_room',
            'code': RoomsErrors.ROOM_CREATION_NOT_ALLOWED
        }}))

    logging.info(f'Creating room "{data.get("name")}"')

    room_id, room_data = RoomsCollection.INSTANCE.create_room(data['name'], data.get('password'), data.get('max_join'))

    WebSocketServer.rooms_instances[room_data['custom_id']] = RoomServer(
            WebSocketServer.INSTANCE.sock,
            room_data=room_data
        )

    client.send(dumps({'type': 'create_confirm', 'data': {
        'position': [0, 0],
        'name': data.get('name'),
        'id': room_id
    }}))

