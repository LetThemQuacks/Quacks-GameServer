from .handler import PacketHandler
from ...client import WebSocketClient
from ...server import WebSocketServer

from src.database.errors import RoomsErrors

from core import logging
from json import dumps

from ....utilities import APIUtils

@PacketHandler.handle(packet_type='join_room')
def join_room(client: WebSocketClient, data: dict) -> dict:
    if not data.get('id') in WebSocketServer.rooms_instances:
        return APIUtils.error('join_room', RoomsErrors.ROOM_NOT_FOUND)

    if client.CURRENT_ROOM:
        old_room = client.CURRENT_ROOM
        old_room.user_left(client)

    room = WebSocketServer.rooms_instances[data.get('id')]
    room.user_join(client)
    client.CURRENT_ROOM = room

    logging.info(f'{client.username} ({client.user_id}) has joined {room.ROOM_DATA["name"]} ({room.ROOM_ID})')

    return {'type': 'join_confirm', 'data': {
        'online': room.online_dict(exclude=client),
        'position': [0, 0]
        }}
