from .handler import PacketHandler, QuickFilters
from ...client import WebSocketClient
from ...server import WebSocketServer

from src.database.collections.rooms.rooms import RoomsCollection
from src.database.errors import RoomsErrors
from src.api.server.game.room import RoomServer
from src.api.server.types.client import Packet

from ....utilities import APIUtils

from core import logging

from configs import configs
import time
 
def check_ratelimit(start: float, end: float) -> bool:
    """
        Returns True if the ratelimit has been reached, otherwise retuns False
    """
    if not configs['room_creation']['ratelimit']['enable']:
        return False

    return (end - start) < configs['room_creation']['ratelimit']['value']


@PacketHandler.handle(packet_type='create_room', filters=[QuickFilters.any_null_value])
def create_room(client: WebSocketClient, data: dict) -> Packet:
    if not configs['room_creation']['allow']:
        return APIUtils.error('create_room', RoomsErrors.ROOM_CREATION_NOT_ALLOWED)

    if check_ratelimit(client.last_room_created, time.time()):
        return APIUtils.error(
            'create_room',
            RoomsErrors.RATELIMIT_REACHED,
            wait = configs['room_creation']['ratelimit']['value'] - (time.time() - client.last_room_created)
        )


    logging.info(f'Creating room "{data.get("name")}" author: ({client.user_id}) {client.username} ')

    room_id, room_data = RoomsCollection.INSTANCE.create_room(
            data['name'], 
            data.get('password'), 
            data.get('max_join'),
            data['ephemeral'] or configs['room_creation']['force_ephemeral'],
    )

    WebSocketServer.rooms_instances[room_data['custom_id']] = RoomServer(
            WebSocketServer.INSTANCE.sock,
            room_data=room_data
        )

    client.last_room_created = time.time()

    return {'type': 'create_confirm', 'data': {
        'position': [0, 0],
        'name': data.get('name'),
        'id': room_id
    }}
