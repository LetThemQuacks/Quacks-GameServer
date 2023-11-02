import secrets
import time
from uuid import uuid4
from src.api.server.game.data.chat import messageConfirm, sendMessage
from src.api.plugins.controller import SmartCallbacks
from src.api.plugins.events.packets.types.message import MessageEvent
from core import logging

logging.debug('Moderator plugin started')

@SmartCallbacks.command('kick')
def kick_command(event: MessageEvent):
    if not event.client.CURRENT_ROOM:
        return

    event.ignore()

    event.client.send(messageConfirm(event.packet['data'].get('req_id'), str(uuid4()), event.client.color, 'hide'))

    if event.client.user_id != event.client.CURRENT_ROOM.owner:
        return event.client.send(sendMessage(str(uuid4()), 'You\'re not an admin', 'ffff', 'Moderator Bot', 'eb4034'))

    cmd_username = event.message.split(' ')[-1]

    if cmd_username == event.client.username:
        return event.client.send(sendMessage(str(uuid4()), 'You can\'t kick yourself out', 'ffff', 'Moderator Bot', 'eb4034'))

    for client in event.client.CURRENT_ROOM.online_users:
        user = client.username

        if user == cmd_username:
            event.client.send(sendMessage(str(uuid4()), f'{user} has been kicked out', 'ffff', 'Moderator Bot'))
            event.client.CURRENT_ROOM.user_left(client)
            client.CURRENT_ROOM = None

            client.send({'type': 'purge', 'data': {}})
            client.send(sendMessage(str(uuid4()), "You've been kicked out of this room.", 'ffff', 'Moderator Bot', 'eb4034'))
            break
    else:
        event.client.send(sendMessage(str(uuid4()), f'Nobody is called "{cmd_username}"', 'ffff', 'Moderator Bot'))

@SmartCallbacks.command('clear')
def clear_chat(event: MessageEvent):
    if not event.client.CURRENT_ROOM: return

    event.ignore()

    event.client.send(messageConfirm(event.packet['data'].get('req_id'), str(uuid4()), event.client.color, 'hide'))
    event.client.send({'type': 'purge', 'data': {}})
