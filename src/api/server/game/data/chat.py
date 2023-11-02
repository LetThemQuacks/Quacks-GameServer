"""
    Setup packet data easly
"""

from typing import Union
from base64 import b64encode

from src.api.server.types.client import Packet

def sendMessage(msg_id: str, content: Union[str, bytes], author_id: str, username: str, color: str = 'efb820', encoded: bool = False) -> Packet:
    if not encoded:
        content = b64encode(content.encode() if isinstance(content, str) else content).decode()

    return {
        'type': 'message',
        'data': {
            'content': content,
            'id': msg_id,
            'author': {
                'id': author_id,
                'username': username,
                'color': color
            }
        }
    }

def messageConfirm(req_id: Union[str, None], msg_id: str, color: str, action: Union[str, None] = None) -> Packet:
    return {
        'type': 'message_confirm',
        'data': {
            'res_id': req_id,
            'msg_id': msg_id,
            'color': color,
            'action': action
        }
    }


