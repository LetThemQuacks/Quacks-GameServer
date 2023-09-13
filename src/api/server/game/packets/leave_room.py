from .handler import PacketHandler
from ...client import WebSocketClient

from src.database.errors import RoomsErrors

from core import logging

from src.api.utilities import APIUtils
from src.api.server.types.client import Packet

@PacketHandler.handle(packet_type='leave_room')
def leave_room(client: WebSocketClient, _) -> Packet:
    if not client.CURRENT_ROOM:
        return APIUtils.error('leave_room', RoomsErrors.MUST_BE_IN_ROOM)

    room_id, room_name = client.CURRENT_ROOM.ROOM_ID, client.CURRENT_ROOM.ROOM_DATA['name']
    client.CURRENT_ROOM.user_left(client)
 
    logging.info(f'{client.username} ({client.user_id}) has left {room_name} ({room_id})')

    return {'type': 'kick', 'data': {
            'room': room_id,
            'reason': 'user_disconnect'
        }}
