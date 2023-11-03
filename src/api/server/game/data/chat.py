"""
    Setup packet data easly
"""

from typing import Union
from base64 import b64encode

from src.api.server.types.client import Packet

# color: str = 'efb820'

def systemMessage(msg_id: str, content: str, color: str = 'efb820', encoded: bool = False) -> Packet:
    if not encoded:
        content = b64encode(content.encode() if isinstance(content, str) else content).decode()

    return {
            'type': 'system_message',
            'data': {
                    'id': msg_id,
                    'content': content,
                    'color': color
                }
            }

def sendMessage(msg_id: str, content: Union[str, bytes], author_id: str, encoded: bool = False, **author_overwrites) -> Packet:
    if not encoded:
        content = b64encode(content.encode() if isinstance(content, str) else content).decode()

    data: Packet = {
        'type': 'message',
        'data': {
            'content': content,
            'id': msg_id,
            'author': {
                'type': 'user',
                'id': author_id
            }
        }
    }
    data['data']['author'].update(author_overwrites)

    return data

def messageConfirm(req_id: Union[str, None], msg_id: str, action: Union[str, None] = None) -> Packet:
    return {
        'type': 'message_confirm',
        'data': {
            'res_id': req_id,
            'msg_id': msg_id,
            'action': action
        }
    }

