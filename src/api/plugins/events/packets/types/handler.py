class PacketEventType:
    packets_callbacks = {'type': {}}

    @staticmethod
    def register(packet_type: str):
        def inner(obj):
            PacketEventType.packets_callbacks['type'][packet_type] = {'event': obj}
            return obj
        return inner

