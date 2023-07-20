from typing import Callable, Union, Tuple

from src.database.errors import ChatErrors, RoomsErrors

"""
Filter: NoneType or a function that requires a WebSocketClient (object) for the first parameter and returns
a tuple with a bool and a str ( if the bool is False ) or NoneType

Function Example:
def filter(client: WebSocketClient):
    if ...:
        return False, 'error'
    return True, None
"""

Filter = Union[
            Callable[
                [object],
                Tuple[bool, Union[
                    str, None
                ]]
            ],
        None]



class PacketHandler:
    packets_callbacks = {'type': {}}

    def handle(packet_type: str, filter: Filter = None):
        def inner(func):
            PacketHandler.packets_callbacks['type'][packet_type] = {'callback': func, 'filter': filter}
            return func
        return inner

class QuickFilters:
    @staticmethod
    def in_room(client: object) -> bool:
        if client.CURRENT_ROOM:
            return True, None
        return False, ChatErrors.MUST_BE_IN_ROOM


