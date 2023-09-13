from .handler import PacketHandler, QuickFilters
from ...client import WebSocketClient

@PacketHandler.handle(packet_type='move', filters=[QuickFilters.in_room])
def movement(client: WebSocketClient, data: dict) -> None:
    # TODO: update duck physics state using the received data

    client.CURRENT_ROOM.broadcast({
        'type': 'move',
        'data': {
            'entity_id': client.user_id,
            'state': client.public_physics_state
        }
    })

