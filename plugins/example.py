from src.api.plugins.controller import CallbacksStorage, SmartCallbacks
from src.api.plugins.events.packets import Packet2ClientEvent, Packet2ServerEvent
from core import logging

logging.debug('[green]█[/][white]█[/][red]█[/] [green]UAAAAAAAAAAAA FRATMO SONO IL PLUGIN SONO STATO IMPORTATO[/]')


@SmartCallbacks.command('ping')
def ping_command(event: Packet2ServerEvent):
    if not event.client.CURRENT_ROOM:
        return

    event.client.send({
        'type': 'message',
        'data': {
            'content': 'Pong!',
            'author': {
                'id': 'ffffffffffffffffffffffff',
                'username': 'Server Bot'
            }
        }
    })

