from time import time_ns
from .handler import PacketHandler, QuickFilters
from ...client import WebSocketClient

@PacketHandler.handle(packet_type='move', filters=[QuickFilters.in_room])
def movement(client: WebSocketClient, data: list) -> None:
    # TODO: update duck physics state using the received data

    client.duck.position = (
        client.duck.position[0] + data[0] * 10,
        client.duck.position[1] + data[1] * 10
    )
    client.CURRENT_ROOM.position_updates[client.user_id] = client.public_physics_state

    last_update = client.CURRENT_ROOM.last_position_update


    if (time_ns() - last_update > 0.05):
        client.CURRENT_ROOM.broadcast({
            'type': 'move',
            'data': {
                'entities': [
                    {'id': ID, 'state': get_state()} \
                        for ID, get_state in client.CURRENT_ROOM.position_updates.items()
                ]
            }
        })
        client.CURRENT_ROOM.last_position_update = time_ns()
