from src.database.errors import ChatErrors
from src.database.collections.chats.chats import ChatsCollection
from src.api.server.client import WebSocketClient
from .handler import PacketHandler, QuickFilters

from src.api.utilities import APIUtils
from src.api.server.types.client import Packet

@PacketHandler.handle(packet_type='load_messages', filters=[QuickFilters.in_room, QuickFilters.has_chat])
def load_messages(client: WebSocketClient, data: dict) -> Packet:
    start, end = data['start'], data['end']

    if abs(end - start) > 50:
        return APIUtils.error('load_messages', ChatErrors.LOAD_TOO_BIG)

    messages = ChatsCollection.INSTANCE.get_messages(client.CURRENT_ROOM.chat, start, end)
    return {'type': 'load_chat', 'data': {
        'chat': messages,
    }}
