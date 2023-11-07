from .handler import PacketHandler, QuickFilters
from ...client import WebSocketClient

from core import logging

from src.api.server.types.client import Packet

@PacketHandler.handle(packet_type='leave_room', filters=[QuickFilters.in_room])
def leave_room(client: WebSocketClient, _) -> Packet:
    left_room = client.CURRENT_ROOM

    client.CURRENT_ROOM.user_left(client)
    client.CURRENT_ROOM = None

    logging.info(f'{client.username} ({client.user_id}) has left {left_room.ROOM_DATA["name"]} ({left_room.ROOM_ID})')

    return {'type': 'kick', 'data': {
            'room': left_room.ROOM_ID,
            'reason': 'user_disconnect'
        }}
