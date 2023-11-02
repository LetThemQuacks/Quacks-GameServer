from .handler import PacketHandler, QuickFilters
from ...client import WebSocketClient

from src.api.utilities import APIUtils 
from src.database.errors import ChatErrors
from src.api.server.types.client import Packet
from src.api.server.game.data.chat import sendMessage

from src.database.collections.chats.chats import ChatsCollection

import uuid

@PacketHandler.handle(packet_type='send_message', filters=[QuickFilters.in_room])
def broadcast_room_message(client: WebSocketClient, data: dict) -> Packet:
    if data.get('message', '').replace(' ', '') == '':
        return APIUtils.error('send_message', ChatErrors.EMPTY_MESSAGE)

    msg_id = str(uuid.uuid4())

    client.CURRENT_ROOM.broadcast(
        sendMessage(msg_id, data['message'], client.user_id, client.username, client.color, True), (client,)
    )

    if client.CURRENT_ROOM.chat:
        ChatsCollection.INSTANCE.add_message(
            client.CURRENT_ROOM.chat,
            msg_id,
            client.user_id, client.username,
            data['message']
        )


    return {
        'type': 'message_confirm',
        'data': {'res_id': data.get('req_id'), 'msg_id': msg_id, 'color': client.color}
    }


