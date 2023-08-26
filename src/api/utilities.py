from typing import Tuple

from .server.types.client import Packet

class APIUtils:
    @staticmethod
    def check_data(data: dict, keys: tuple) -> bool:
        """
            Checks if all keys are passed in a dict
        """
        for key in keys:
            if '.' in key:
                current = data
                for subkey in key.split('.'):
                    if not subkey in current:
                        return False
                    current = current[subkey]

            else:
                if not key in data:
                    return False
        return True

    @staticmethod
    def error(from_packet_type: str, error_code: str, **additional_data: dict) -> Packet:
        """
            Create a Quacks error using the packet type and the error code
        """
        data = {
            'from_packet_type': from_packet_type,
            'code': error_code
        }
        data.update(additional_data)
        return {'type': 'error', 'data': data}
