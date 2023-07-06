from typing import Tuple

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
    def compile_error(message: str, error_type: str, status_code: int = 400) -> Tuple[dict, int]:
        """
            Returns a formatted error.

            :Arguments:
            - `message`: The error message
            - `error_type`: The type of the error. accepted values: "debug", "user"
        """
        return {'err': True, 'type': error_type, 'msg': message}, status_code
