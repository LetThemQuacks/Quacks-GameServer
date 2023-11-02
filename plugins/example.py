import base64
from uuid import uuid4
from src.api.server.game.data.chat import messageConfirm, sendMessage
from src.api.plugins.controller import SmartCallbacks
from src.api.plugins.events.packets import Packet2ServerEvent
from core import logging

logging.debug('[green]█[/][white]█[/][red]█[/] [green][/]')


@SmartCallbacks.command('ping')
def ping_command(event: Packet2ServerEvent):
    if not event.client.CURRENT_ROOM:
        return

    event.ignore() # Ignore the Message Event ( the message will not be broadcasted )

    # Confirm to the client that the message has been processed by the server.
    # This is necessary because the message event has been ignored, so the 
    # Server internal callback will not confirm the message by itself.
    # NOTE: When the client receives the message confirmation it removes the
    #       Loading state from the message in the UI

    event.client.send(messageConfirm(event.packet['data'].get('req_id'), str(uuid4()), event.client.color, 'hide'))

    event.client.send(sendMessage(str(uuid4()), 'Pong!', 'ffff', 'Bot'))

