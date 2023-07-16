class PacketHandler:
    packets_callbacks = {'p_type': {}}

    def handle(p_type: str):
        def inner(func):
            PacketHandler.packets_callbacks['p_type'][p_type] = {'callback': func}
            return func
        return inner


