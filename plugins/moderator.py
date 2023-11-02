import secrets
import time
from uuid import uuid4
from src.api.server.game.data.chat import sendMessage
from src.api.plugins.controller import SmartCallbacks
from src.api.plugins.events.packets.types.message import MessageEvent
from core import logging

logging.debug('Moderator plugin started')

@SmartCallbacks.command('kick')
def kick_command(event: MessageEvent):
    if not event.client.CURRENT_ROOM:
        return

    event.ignore()

    event.client.send({
        'type': 'message_confirm',
        'data': {
            'res_id': event.packet['data'].get('req_id'),
            'action': 'hide' # Hides the message from the chat
        }
    })

    cmd_username = event.message.split(' ')[-1]

    for client in event.client.CURRENT_ROOM.online_users:
        user = client.username

        if user == cmd_username:
            event.client.send(sendMessage(str(uuid4()), f'{user} has been kicked out', 'ffff', 'Moderator Bot'))
            event.client.CURRENT_ROOM.user_left(client)
            client.CURRENT_ROOM = None

            client.send({'type': 'purge', 'data': {}})
            client.send(sendMessage(str(uuid4()), "You've been kicked out of this room.", 'ffff', 'Moderator Bot', 'efb820'))
            break
    else:
        event.client.send(sendMessage(str(uuid4()), f'Nobody is called "{cmd_username}"', 'ffff', 'Moderator Bot'))

