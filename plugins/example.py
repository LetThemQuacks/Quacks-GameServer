import base64
import time
from uuid import uuid4
from src.api.plugins.controller import CallbacksStorage, SmartCallbacks
from src.api.plugins.events.packets import Packet2ClientEvent, Packet2ServerEvent
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

    event.client.send({
        'type': 'message_confirm',
        'data': {
            'res_id': event.packet['data'].get('req_id'),
            'action': 'hide' # Hides the message from the chat
        }
    })

    event.client.send({
        'type': 'message',
        'data': {
            'content': base64.b64encode(b'Pong!').decode(),
            'id': str(uuid4()),
            'author': {
                'id': 'ffff',
                'username': 'Bot'
            }
        }
    })

