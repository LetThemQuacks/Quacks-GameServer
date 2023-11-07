from .handler import PacketHandler, QuickFilters
from ...client import WebSocketClient

from src.api.utilities import APIUtils 
from src.database.errors import ChatErrors
from src.api.server.types.client import Packet

from src.database.collections.chats.chats import ChatsCollection

@PacketHandler.handle(packet_type='delete_message', filters=[QuickFilters.in_room, QuickFilters.has_chat])
def broadcast_room_message(client: WebSocketClient, data: dict) -> Packet:
    message = ChatsCollection.INSTANCE.find_message(client.CURRENT_ROOM.chat, data['message_id'])

    if message is None:
        return APIUtils.error('delete_message', ChatErrors.MESSAGE_NOT_FOUND)

    ChatsCollection.INSTANCE.delete_message(client.CURRENT_ROOM.chat, message)

    return {'type': 'delete_message', 'data': {'id': message['data']['id']}}

