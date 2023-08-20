from .handler import PacketHandler, QuickFilters
from ...client import WebSocketClient
from ...server import WebSocketServer

from src.database.errors import RoomsErrors

from core import logging
from json import dumps


@PacketHandler.handle(packet_type='move', filters=[QuickFilters.in_room])
def movement(client: WebSocketClient, data: dict) -> None:
    # TODO: update duck physics state using the received data

    client.CURRENT_ROOM.broadcast(dumps({
        'type': 'move',
        'data': {
            'entity_id': client.user_id,
            'state': client.public_physics_state
        }
    }))

