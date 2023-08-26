from ._structure import PacketEvent

from src.api.server.types.client import Packet

class Packet2ClientEvent(PacketEvent):
    ignored = False
    direction = 'S2C'

    def __init__(self, packet: Packet, client):
        self.packet = packet
        self.client = client

    def ignore(self):
        self.ignored = True

    def __repr__(self):
        return dict(packet=self.packet, client=self.client, direction=self.direction)

    def __str__(self):
        return f'Packet2ClientEvent(packet={self.packet}, client={self.client})'
