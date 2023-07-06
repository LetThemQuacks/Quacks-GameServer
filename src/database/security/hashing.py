from typing import Callable, Union
import hashlib

def hash_password(password: str,
                  salt: Union[bytes, None] = None,
                  hashing_function: Callable = hashlib.sha3_512,
                  work_factors: int = 3,
        ) -> str:

    result_hash: bytes = password.encode()
    for _ in range(work_factors):
        result_hash: bytes = hashing_function(
            result_hash + (salt if salt else b'')
        ).hexdigest().encode()

    return result_hash.decode()


