import functools
import base64
from typing import List, Callable, Union
import os
from src.api.plugins.events.packets.client import Packet2ClientEvent
from src.api.plugins.events.packets.server import Packet2ServerEvent

from ..server.types.client import Packet
from core import logging

# Callback Info
class PacketDirection: 
    FROM_CLIENT = 'C2S' # Client to Server
    FROM_SERVER = 'S2C' # Server to Client
    TO_SERVER = 'C2S' # Client to Server
    TO_CLIENT = 'S2C' # Server to Client
    ALL = '*'

    accepted_directions = (FROM_CLIENT, FROM_SERVER, ALL)
    real_directions = (FROM_CLIENT, FROM_SERVER)

class CallbacksStorage:
    loading_plugin = None
    INSTANCE = None
    _registered_callbacks = {}

    for direction in PacketDirection.real_directions:
        _registered_callbacks[direction] = {'type': {}}

    """
    
    _registered_callbacks example value:
    {
        "C2S": {
            "type": {
                "send_message": {
                    "callbacks": [
                        {
                            "callback": <function hello_command at 0x0......>,
                            "data_filters": {"content": "!hello"}
                        }
                    ]
                }
            }
        },
        "S2C": {
            "type": {}
        }
    }

    """

    def __init__(self):
        if CallbacksStorage.INSTANCE:
            raise RuntimeError('CallbacksStorage object is based on the singletone design pattern: it has already been initialized.')
        CallbacksStorage.INSTANCE = self

    @staticmethod
    def register_callback(packet_type: str, data_filters: dict, direction: str, callback: Callable, plugin_name: Union[str, None] = None) -> None:
        """
            Registers a callback

            :Arguments:
            - `packet_type`: The packet type of the websocket
            - `data_filters`: Call the callback only if the values of the data are the same as the values specified in data_filters
            - `direction`: The packet direction (FROM_CLIENT, FROM_SERVER or ALL)
            - `callback`: The function to call
            - `plugin_name`: Custom plugin name, None: get from CallbacksStorage.loading_plugin
        """
        if not direction in PacketDirection.accepted_directions:
            raise ValueError(f'The direction value must be one of these: {PacketDirection.accepted_directions}')

        registered_directions = (direction,) if direction != PacketDirection.ALL else PacketDirection.real_directions

        for direction in registered_directions:
            if not packet_type in CallbacksStorage._registered_callbacks[direction]['type']:
                CallbacksStorage._registered_callbacks[direction]['type'][packet_type] = {'callbacks': []}

            CallbacksStorage._registered_callbacks[direction]['type'][packet_type]['callbacks'].append({
                'callback': callback,
                'data_filters': data_filters,
                'plugin': CallbacksStorage.loading_plugin
            })

        logging.debug(CallbacksStorage._registered_callbacks)

    @staticmethod
    def cancel_callback(callback_filter: dict, callback_type: str = 'websocket') -> None:
        """
            Un-register a callback.

            :Arguments:
            - `callback_filter`: Filter of the callback, for example: {"packet": 1} or {"endpoint": "/send_message"}
            - `callback_type`: The type of the callback, default: websocket
        """
        if not callback_type in CallbacksStorage._registered_callbacks.keys():
            raise ValueError(f'The registered callback must be one of those values: {tuple(CallbacksStorage._registered_callbacks.keys())}')

        for filter_key, filter_value in callback_filter.items():
            if filter_key in CallbacksStorage._registered_callbacks and filter_value in CallbacksStorage._registered_callbacks[callback_type]:
                CallbacksStorage._registered_callbacks[callback_type][filter_key].pop(filter_value)

    @staticmethod
    def iter_callbacks(event: Union[Packet2ServerEvent, Packet2ClientEvent]) -> None:
        if not event.packet['type'] in CallbacksStorage._registered_callbacks[event.direction]['type']:
            return

        for callback in CallbacksStorage._registered_callbacks[event.direction]['type'][event.packet['type']]['callbacks']:
            for key, value in callback['data_filters'].items():
                if event.packet['data'].get(key) != value:
                    return

            try:
                callback['callback'](event)
            except Exception:
                logging.exception(f'Plugin [yellow]{callback["plugin"]}[/] failed to handle packet {event.packet["type"]}')

    @staticmethod
    def ws_event(packet_type: str, filters: dict = {}, direction: str = PacketDirection.FROM_CLIENT) -> Callable:
        def inner(function: Callable):
            CallbacksStorage.register_callback(packet_type, filters, direction, function)
            return function
        return inner


class SmartCallbacks:
    on_message = CallbacksStorage.ws_event('send_message')
    on_move    = CallbacksStorage.ws_event('move')
    on_join    = CallbacksStorage.ws_event('join_room')
    
    @staticmethod
    def _command_callback(command_prefix, command_name, callback, event):
        content = base64.b64decode(event.packet['data']['message']).decode('utf-8')

        if content.startswith(f'{command_prefix}{command_name}'):
            callback(event)

    @staticmethod
    def command(name: str, prefix: str = ':'):
        def inner(function: Callable):
            CallbacksStorage.ws_event('send_message')(
                functools.partial(SmartCallbacks._command_callback, prefix, name, function)
            )
            return function
        return inner


class PluginController:
    def __init__(self) -> None:
        pass

    def _list_plugins_files(self) -> List[str]:
        """
            Helper function for load_plugins()
            List plugin files            
        """
        return [plugin[:-3] for plugin in os.listdir('./plugins') if plugin.endswith('.py')]

    def _init_plugin(self, instance: Callable) -> None:
        """
            Helper function for load_plugins()
            Used for initialization of the plugin object
        """
        pass # TODO

    def load_plugins(self) -> None:
        """
            Import and initialize plugin files from the /plugins directory
        """
        for plugin in self._list_plugins_files():
            logging.info(f'Loading [yellow]{plugin}[/] plugin')
            CallbacksStorage.loading_plugin = plugin
            try:
                __import__(f'plugins.{plugin}')
            except Exception as e:
                logging.exception(f'Error encountered while loading the [yellow]{plugin}[/] plugin:')
            else:
                logging.info(f'[green]Succesfully[/] loaded plugin [yellow]{plugin}[/]')

        CallbacksStorage.loading_plugin = None

        # TODO: Finish this function
