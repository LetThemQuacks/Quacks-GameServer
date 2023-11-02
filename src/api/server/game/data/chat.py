"""
    Setup packet data easly
"""

from typing import Union
from base64 import b64encode

from src.api.server.types.client import Packet

def sendMessage(msg_id: str, content: Union[str, bytes], author_id: str, username: str) -> Packet:
    return {
        'type': 'message',
        'data': {
            'content': b64encode(content.encode() if isinstance(content, str) else content).decode(),
            'id': msg_id,
            'author': {
                'id': author_id,
                'username': username
            }
        }
    }

def messageConfirm(req_id: Union[str, None], msg_id: str):
    return {
        'type': 'message_confirm',
        'data': {
            'res_id': req_id,
            'msg_id': msg_id
        }
    }


