from .handler import PacketHandler, QuickFilters
from ...client import WebSocketClient

from src.api.utilities import APIUtils 
from src.database.errors import ChatErrors
from src.api.server.types.client import Packet
from src.api.server.game.data.chat import messageConfirm, sendMessage

from src.database.collections.chats.chats import ChatsCollection

import uuid

@PacketHandler.handle(packet_type='send_message', filters=[QuickFilters.in_room])
def broadcast_room_message(client: WebSocketClient, data: dict) -> Packet:
    if data.get('message', '').replace(' ', '') == '':
        return APIUtils.error('send_message', ChatErrors.EMPTY_MESSAGE)

    msg_id = str(uuid.uuid4())
    msg_data = sendMessage(msg_id, data['message'], client.user_id, True)

    client.CURRENT_ROOM.send_message(msg_data, (client,))

    return messageConfirm(data.get('req_id'), msg_id)

