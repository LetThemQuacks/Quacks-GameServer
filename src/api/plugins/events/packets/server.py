from ._structure import PacketEvent

from src.api.server.types.client import Packet

from core import logging

class Packet2ServerEvent(PacketEvent):
    ignored = False
    direction = 'C2S'

    def __init__(self, packet: Packet, client):
        self.packet = packet
        self.client = client

    def ignore(self):
        self.ignored = True

    def __repr__(self):
        return dict(packet=self.packet, client=self.client, direction=self.direction)

    def __str__(self):
        return f'Packet2ServerEvent(packet={self.packet}, client={self.client})'
