from functools import partial
import secrets
import threading
from uuid import uuid4
from src.api.server.game.data.chat import messageConfirm, sendMessage
from src.api.plugins.controller import SmartCallbacks
from src.api.plugins.events.packets.types.message import MessageEvent
from core import logging

from src.database.collections.chats.chats import ChatsCollection
from bson import ObjectId

logging.debug('Moderator plugin started')

botMessage = partial(sendMessage, author_id='ffff', username='Moderator Bot', color='efb820')

@SmartCallbacks.command('kick')
def kick_command(event: MessageEvent):
    if not event.client.CURRENT_ROOM:
        return

    event.ignore()

    event.client.send(messageConfirm(event.packet['data'].get('req_id'), str(uuid4()), 'hide'))

    if event.client.user_id != event.client.CURRENT_ROOM.owner:
        return event.client.send(botMessage(str(uuid4()), 'You\'re not an admin', color='eb4034'))

    cmd_username = event.message.split(' ')[-1]

    if cmd_username == event.client.username:
        return event.client.send(botMessage(str(uuid4()), 'You can\'t kick yourself out', color='eb4034'))

    for client in event.client.CURRENT_ROOM.online_users:
        user = client.username

        if user == cmd_username:
            event.client.send(botMessage(str(uuid4()), f'{user} has been kicked out'))
            event.client.CURRENT_ROOM.user_left(client)
            client.CURRENT_ROOM = None

            client.send({'type': 'purge', 'data': {}})
            client.send(botMessage(str(uuid4()), "You've been kicked out of this room.", color='eb4034'))
            break
    else:
        event.client.send(botMessage(str(uuid4()), f'Nobody is called "{cmd_username}"'))

@SmartCallbacks.command('clearview')
def clear_chat(event: MessageEvent):
    """
        Clear the message list UI ( only for the executer )
    """
    if not event.client.CURRENT_ROOM: return

    event.ignore()

    event.client.send(messageConfirm(event.packet['data'].get('req_id'), str(uuid4())))
    event.client.send({'type': 'purge', 'data': {}})

@SmartCallbacks.command('crash')
def crash(event: MessageEvent):
    event.client.send({'type': 'message', 'data': 0})

@SmartCallbacks.command('cleardb')
def clear_chat_database(event: MessageEvent):
    """
        Clear the chat messages for everyone & in the database ( if there's one )
    """

    if not event.client.CURRENT_ROOM: return

    event.ignore()

    event.client.send(messageConfirm(event.packet['data'].get('req_id'), str(uuid4()), 'hide'))

    if event.client.user_id != event.client.CURRENT_ROOM.owner:
        return event.client.send(botMessage(str(uuid4()), 'You\'re not an admin', color='eb4034'))

    for client in event.client.CURRENT_ROOM.online_users:
        client.send({'type': 'purge', 'data': {}})
        client.send(botMessage(str(uuid4()), "The chat has been purged by a moderator"))

    chat_id = event.client.CURRENT_ROOM.chat
    if chat_id:
        ChatsCollection.INSTANCE.collection.update_one({'_id': ObjectId(chat_id)}, {'$set': {'messages': []}})

