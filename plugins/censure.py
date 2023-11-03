from uuid import uuid4
from src.api.plugins.events.packets.types.message import MessageEvent
from src.api.server.game.data.chat import messageConfirm, sendMessage
from src.api.plugins.controller import CallbacksStorage
from src.api.plugins.events.packets import Packet2ServerEvent
from core import logging

logging.debug('[green]█[/][white]█[/][red]█[/] [green][/]')


@CallbacksStorage.ws_event('send_message')
def ping_command(event: MessageEvent):
    if not event.client.CURRENT_ROOM:
        return


    if 'fuck' in event.message:
        event.ignore()
        event.client.send(messageConfirm(event.packet['data'].get('req_id'), str(uuid4()), 'hide'))

        event.client.send(sendMessage(str(uuid4()), "You can't say that!", 'ffff', username='Bot', color='eb4034'))

