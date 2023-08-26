from typing import Union

from src.api.server.types.client import Packet
from .packets import Packet2ServerEvent, Packet2ClientEvent

class EventFactory:
    direction_objects = {
        'C2S': Packet2ServerEvent,
        'S2C': Packet2ClientEvent
    }

    def __new__(cls, direction: str, packet: Packet, client) -> Union[Packet2ServerEvent, Packet2ClientEvent, None]:
        if not direction in EventFactory.direction_objects:
            raise ValueError(f'Unknown Direction: {direction} (known directions: {tuple(EventFactory.direction_objects.keys())})')

        return EventFactory.direction_objects[direction](packet, client)

