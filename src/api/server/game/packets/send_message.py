from .handler import PacketHandler, QuickFilters
from ...client import WebSocketClient
from ...server import WebSocketServer

from src.database.errors import ChatErrors

from core import logging
from json import dumps

@PacketHandler.handle(packet_type='send_message', filters=[QuickFilters.in_room])
def broadcast_room_message(client: WebSocketClient, data: dict) -> None:
    if data.get('message', '').replace(' ', '') == '':
        return client.send(dumps({'type': 'error', 'data': {
            'from_packet_type': 'join_room',
            'code': ChatErrors.EMPTY_MESSAGE
        }}))

    client.CURRENT_ROOM.broadcast(dumps({
        'type': 'message',
        'data': {
            'content': data.get('message'),
            'author': {
                'id': client.user_id,
                'username': client.username
            }
        }
    }))
