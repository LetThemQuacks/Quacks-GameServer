from typing import Union, List

from .....database.errors import ChatErrors, DataErrors

from ...types.client import CallbackFilter, CallbacksStorage

class PacketHandler:
    packets_callbacks: CallbacksStorage = {'type': {}}

    @staticmethod
    def handle(packet_type: str, filters: List[CallbackFilter] = []):
        def inner(func):
            PacketHandler.packets_callbacks['type'][packet_type] = {'callback': func, 'filters': filters}
            return func
        return inner

class QuickFilters:
    @staticmethod
    def in_room(client, packet) -> Union[str, bool]:
        if client.CURRENT_ROOM:
            return True
        return ChatErrors.MUST_BE_IN_ROOM

    @staticmethod
    def any_null_value(client, packet) -> Union[str, bool]:
        data = packet['data']
        for key, value in data.items():
            if not value:
                return DataErrors.NULL
        return True
