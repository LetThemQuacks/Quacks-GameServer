from .handler import PacketHandler
from ...client import WebSocketClient
from ...server import WebSocketServer

from src.database.errors import RoomsErrors

from core import logging
from json import dumps

 
@PacketHandler.handle(packet_type='join_room')
def join_room(client: WebSocketClient, data: dict) -> None:
    if not data.get('id') in WebSocketServer.rooms_instances:
        return client.send(dumps({'type': 'error', 'data': {
            'from_packet_type': 'join_room',
            'code': RoomsErrors.ROOM_NOT_FOUND
        }}))

    if client.CURRENT_ROOM:
        old_room = client.CURRENT_ROOM
        old_room.user_left(client)

    room = WebSocketServer.rooms_instances[data.get('id')]
    room.user_join(client)
    client.CURRENT_ROOM = room

    client.send(dumps({'type': 'join_confirm', 'data': {
        'online': room.online_dict(exclude=client),
        'position': [0, 0]
    }}))
