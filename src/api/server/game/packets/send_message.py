from .handler import PacketHandler, QuickFilters
from ...client import WebSocketClient

from src.api.utilities import APIUtils 
from src.database.errors import ChatErrors
from src.api.server.types.client import Packet

from json import dumps
from typing import Union
import uuid

@PacketHandler.handle(packet_type='send_message', filters=[QuickFilters.in_room])
def broadcast_room_message(client: WebSocketClient, data: dict) -> Union[Packet, None]:
    if data.get('message', '').replace(' ', '') == '':
        return APIUtils.error('send_message', ChatErrors.EMPTY_MESSAGE)

    if not client.CURRENT_ROOM: return

    message_data: Packet = {
        'type': 'message',
        'data': {
            'content': data.get('message'),
            'id': str(uuid.uuid4()),
            'author': {
                'id': client.user_id,
                'username': client.username
            }
        }
    }

    client.CURRENT_ROOM.broadcast(message_data, (client,))
    message_data['data'].update({'res_id': data.get('req_id')})
    client.send(message_data)


