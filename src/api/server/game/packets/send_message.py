from .handler import PacketHandler, QuickFilters
from ...client import WebSocketClient
from ...server import WebSocketServer

from ....utilities import APIUtils 

from src.database.errors import ChatErrors

from core import logging
from json import dumps

from typing import Union

@PacketHandler.handle(packet_type='send_message', filters=[QuickFilters.in_room])
def broadcast_room_message(client: WebSocketClient, data: dict) -> Union[dict, None]:
    if data.get('message', '').replace(' ', '') == '':
        return APIUtils.error('send_message', ChatErrors.EMPTY_MESSAGE)

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
