from simple_websocket.ws import Server

from dataclasses import asdict
from flask import request
from core import logging

from .crypto_algorithms.RSA import RSACipher
from .crypto_algorithms.AES import AESCipher

from .game.packets.handler import PacketHandler, PacketsPhases
from .game.physics.duck import Duck
from .game.room import RoomServer

from .types.client import Packet
from typing import Union

from ..plugins.controller import CallbacksStorage, PacketDirection, PluginController
from ..plugins.events.factory import EventFactory

import threading
import json
import time
import random

from simple_websocket.ws import ConnectionClosed

null_packet: Packet = {'type': None, 'data': {}}
null_packet_string  = json.dumps(null_packet)

def random_color():
    return ''.join([hex(random.randint(100, 200))[2:] for _ in range(3)])

class WebSocketClient:
    RSA_INSTANCE: Union[RSACipher, None]  = None
    AES_INSTANCE: Union[AESCipher, None]  = None
    CURRENT_ROOM: RoomServer = None
    INTEGRITY: dict = {'aes': None, 'rsa': None, 'said': None, 'intact': False}

    connected = True
    last_room_created = 0
    phase = PacketsPhases.PRE_CRYPTO
    
    last_room_created: float = 0.0

    def __init__(self, ws: Server):
        self.ws = ws
        self.addr = request.remote_addr
        self.args = request.args
        self.start_time = time.time()
        self.duck = Duck()
        self.color = random_color()

        logging.info(f'WS Client Connected from {self.addr}')
        logging.debug(f'WebSocket Connection Arguments: {self.args}')
        logging.debug(f'Running a new packet handler for {self.addr}, Total Threads Count: {threading.active_count()}')
        self.handle_packets()
        

    def setup_user_info(self, user_id: str, username: str, skin: str) -> None:
        self.user_id = user_id
        self.username = username
        self.skin = skin

    def _check_filters(self, filters, packet):
        for filter_callback in filters:
            result = filter_callback(self, packet)
            if isinstance(result, str):
                self.send({'type': 'error', 'data': {
                    'from_packet_type': packet['type'],
                    'code': result
                }})
                return False

        return True

    def _compare_phase(self, callback):
        return self.phase == callback['wphase']

    def _call_callback(self, callback, packet: Packet) -> None:
        logging.debug(f'Calling callback {callback.get("callback")}')
        return callback.get('callback')(self, packet.get('data', {}))

    def _call_callback_with_filters(self, callback, packet: Packet) -> None:
        filter_check = self._check_filters(callback['filters'], packet)

        if filter_check:
            return self._call_callback(callback, packet)
        else:
            logging.warning(f'Callback "{packet["type"]}" not called [cyan]<-[/] filters check: {filter_check}')

    def handle_packets(self):
        while self.connected:
            packet: Packet = self.load_packet_json(self.recv())
            logging.debug(f'RECV: {packet}')

            event = EventFactory(PacketDirection.FROM_CLIENT, packet, self)
            if event:
                CallbacksStorage.iter_callbacks(event)

                if event.ignored:
                    continue


            try:
                self._internal_packet_handler(packet)
            except Exception:
                logging.exception(f'Failed to handle packet: {packet}')
 
    def _internal_packet_handler(self, packet: Packet) -> None:
        callback = PacketHandler.packets_callbacks['type'].get(packet['type'])
        if not callback:
            return

        phase_check = self._compare_phase(callback)
        if not phase_check:
            return logging.warning(f'{self.addr} ([i]phase {self.phase}[/]) tried to call [cyan]{packet["type"]}[/] ([i]phase {callback["wphase"]}[/])')

        if callback.get('filters'):
            response = self._call_callback_with_filters(callback, packet)
        else:
            response = self._call_callback(callback, packet)

        if isinstance(response, dict):
            self.send(response)


    def load_packet_json(self, string: Union[str, None]) -> Packet:
        string = str(string)
        try:
            return json.loads(string)
        except Exception:
            logging.exception(f'Json parsing [red]FAILED[/]: "{string}"')
            return null_packet

    def recv(self):
        raw_data = self.ws.receive()

        if not raw_data:
            return null_packet_string

        if self.AES_INSTANCE:
            try:
                data = self.AES_INSTANCE.decrypt(raw_data)
            except Exception:
                logging.exception(f'{self.addr} Data decryption FAILED: "{raw_data}"')
                return null_packet_string
            else:
                logging.debug(f'+ Decrypted Data: {data}')
                return data

        return raw_data

    def send(self, data: Packet) -> bool:
        logging.debug(f'SEND: {data}')
        event = EventFactory(PacketDirection.FROM_SERVER, data, self)
        if event:
            CallbacksStorage.iter_callbacks(event)

            if event.ignored:
                return

        try:
            if self.AES_INSTANCE:
                return self.ws.send(self.AES_INSTANCE.encrypt(json.dumps(data)))
            self.ws.send(json.dumps(data))
        except ConnectionClosed:
            self.close()
            return False
        else:
            return True

    def close(self):
        logging.warning(f'Closing connection from {self.addr} ({getattr(self, "user_id", None)})')
        self.connected = False
        if self.CURRENT_ROOM:
            self.CURRENT_ROOM.user_left(self)

        try:
            self.ws.close()
        except: pass

    def jsonify(self):
        return {
            'id': self.user_id,
            'username': self.username,
            'skin': self.skin,
            'state': self.public_physics_state(),
            'color': self.color
        }

    def public_physics_state(self):
        state = asdict(self.duck)
        state.pop('max_velocity')
        state.pop('radius')
        return state

    def __eq__(self, value):
        if isinstance(value, str):
            return value == self.user_id
        elif isinstance(value, WebSocketClient):
            return super().__eq__(value)

