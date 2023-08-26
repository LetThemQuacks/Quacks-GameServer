from abc import ABC, abstractmethod

class PacketEvent(ABC):
    @abstractmethod
    def __init__(self, packet, client):
        pass

    @abstractmethod
    def ignore(self):
        pass
