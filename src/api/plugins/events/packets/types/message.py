from src.api.plugins.events.packets.server import Packet2ServerEvent
from src.api.plugins.events.packets.types.handler import PacketEventType

import base64
from core import logging


@PacketEventType.register('send_message')
class MessageEvent(Packet2ServerEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        logging.debug('STOCAZZOOOOOOOO')
        self.message = base64.b64decode(self.packet['data']['message'].encode()).decode('utf-8')

