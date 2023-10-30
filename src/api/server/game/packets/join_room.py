from src.database.collections.chats.chats import ChatsCollection
from .handler import PacketHandler
from ...client import WebSocketClient
from ...server import WebSocketServer

from src.database.errors import RoomsErrors

from core import logging

from src.api.utilities import APIUtils
from src.api.server.types.client import Packet

@PacketHandler.handle(packet_type='join_room')
def join_room(client: WebSocketClient, data: dict) -> Packet:
    if not data.get('id') in WebSocketServer.rooms_instances:
        return APIUtils.error('join_room', RoomsErrors.ROOM_NOT_FOUND)

    room = WebSocketServer.rooms_instances[data.get('id')]

    if client in room:
        return APIUtils.error('join_room', RoomsErrors.ALREADY_CONNECTED)

    if client.user_id in room:
        connected = room[client.user_id].send({'type': 'ping', 'data': {}})
        if connected: return APIUtils.error('join_room', RoomsErrors.ANOTHER_SESSION_CONNECTED)

    if client.CURRENT_ROOM:
        old_room = client.CURRENT_ROOM
        old_room.user_left(client)

    room.user_join(client)

    logging.info(f'{client.username} ({client.user_id}) has joined {room.ROOM_DATA["name"]} ({room.ROOM_ID})')


    join_confirm: Packet = {'type': 'join_confirm', 'data': {
        'online': room.online_dict(exclude=client),
        'position': [0, 0],
    }}

    if room.chat:
        join_confirm['data'].update({'messages': ChatsCollection.INSTANCE.get_messages(room.chat, -50)})

    return join_confirm
