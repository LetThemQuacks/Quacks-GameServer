from typing import Tuple

from .server.types.client import Error

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
    def compile_error(message: str, error_type: str, status_code: int = 400) -> Tuple[Error, int]:
        """
            Returns a formatted error.

            :Arguments:
            - `message`: The error message
            - `error_type`: The type of the error. accepted values: "debug", "user"
        """
        return {'err': 1, 'type': error_type, 'msg': message}, status_code
