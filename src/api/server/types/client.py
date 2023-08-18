from typing import Tuple, TypedDict, Union, List, Callable, Dict

Vector = Tuple[float, float]

CallbackFilter = Callable[
    [object, dict],
    Union[str, bool]
]


Packet = TypedDict('Packet', {
    'type': Union[str, None],
    'data': dict
})

Error = TypedDict('Error', {
    'err': bool,
    'type': str,
    'msg': str
})

CallbackDict = TypedDict('Callback', {
    'callback': Callable,
    'filters': List[CallbackFilter]
})

CallbacksStorage = TypedDict('CallbacksStorage', {
    'type': Dict[str, CallbackDict]
})
