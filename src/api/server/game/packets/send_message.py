from .handler import PacketHandler, QuickFilters
from ...client import WebSocketClient

from src.api.utilities import APIUtils 
from src.database.errors import ChatErrors, RoomsErrors
from src.api.server.types.client import Packet

from json import dumps
from typing import Union
import uuid

@PacketHandler.handle(packet_type='send_message', filters=[QuickFilters.in_room])
def broadcast_room_message(client: WebSocketClient, data: dict) -> Packet:
    if data.get('message', '').replace(' ', '') == '':
        return APIUtils.error('send_message', ChatErrors.EMPTY_MESSAGE)

    if not client.CURRENT_ROOM:
        return APIUtils.error('send_message', RoomsErrors.MUST_BE_IN_ROOM)

    client.CURRENT_ROOM.broadcast({
        'type': 'message',
        'data': {
            'content': data.get('message'),
            'id': str(uuid.uuid4()),
            'author': {
                'id': client.user_id,
                'username': client.username
            }
        }
    }, (client,))

    return {
        'type': 'message_confirm',
        'data': {'res_id': data.get('req_id')}
    }


