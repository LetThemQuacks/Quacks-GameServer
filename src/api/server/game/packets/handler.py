from typing import Union, List

from src.database.errors import ChatErrors, DataErrors, RoomsErrors

from ...types.client import CallbackFilter, CallbacksStorage


class PacketsPhases:
    PRE_CRYPTO  = 1
    PRE_SAID    = 2
    OPERATIONAL = 3


class PacketHandler:
    packets_callbacks: CallbacksStorage = {'type': {}}

    @staticmethod
    def handle(packet_type: str, filters: List[CallbackFilter] = [], working_phase: int = PacketsPhases.OPERATIONAL):
        def inner(func):
            PacketHandler.packets_callbacks['type'][packet_type] = {'callback': func, 'filters': filters, 'wphase': working_phase}
            return func
        return inner

class QuickFilters:
    @staticmethod
    def in_room(client, packet) -> Union[str, bool]:
        if client.CURRENT_ROOM:
            return True
        return RoomsErrors.MUST_BE_IN_ROOM

    @staticmethod
    def any_null_value(client, packet) -> Union[str, bool]:
        data = packet['data']
        for value in data.values():
            if not value:
                return DataErrors.NULL
        return True
