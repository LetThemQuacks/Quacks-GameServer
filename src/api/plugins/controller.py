from typing import List, Callable
import traceback
import functools
import os

from core import logging


class CallbacksStorage:
    INSTANCE = None
    _registered_callbacks = {
        'websocket': {},
    }

    """
    
    _registered_callbacks example value:
    {
        "websocket": {
            "packet": {
                1: <function hello_callback at 0x0......>
            }
        }
    }

    """

    def __init__(self):
        if CallbacksStorage.INSTANCE:
            raise RuntimeError('CallbacksStorage object is based on the singletone design pattern: it has already been initialized.')
        CallbacksStorage.INSTANCE = self

    @staticmethod
    def register_callback(callback_filter: dict, callback: Callable, callback_type: str = 'websocket') -> None:
        """
            Registers a callback

            :Arguments:
            - `callback_filter`: Filter of the callback, for example: {"packet": 1} or {"endpoint": "/send_message"}
            - `callback`: The callback function.
            - `callback_type`: The type of the callback, default: websocket
        """
        if not callback_type in CallbacksStorage._registered_callbacks.keys():
            raise ValueError(f'The registered callback must be one of those values: {tuple(CallbacksStorage._registered_callbacks.keys())}')


        for filter_key, filter_value in callback_filter.items():
            CallbacksStorage._registered_callbacks[callback_type][filter_key][filter_value] = callback

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
    def websocket_callback(callback_filter):
        def inner(function):
            CallbacksStorage.register_callback(callback_filter, function)
            return function
        return inner


class SmartCallbacks:
    ...


class PluginController:
    def __init__(self) -> None:
        pass

    def _list_plugins_files(self) -> List[str]:
        """
            Helper function for load_plugins()
            List plugin files            
        """
        return [plugin[:-3] for plugin in os.listdir() if plugin.endswith('.py')]

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
            try:
                instance = __import__(f'plugins.{plugin}')
            except Exception as e:
                traceback.print_exc()
            else:
                logging.debug('Succesfully imported plugin "{plugin}"')

        # TODO: Finish this function
