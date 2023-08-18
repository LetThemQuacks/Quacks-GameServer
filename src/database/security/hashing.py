from typing import Callable, Union
import hashlib

import quacks

def hash_password(password: str,
                  salt: Union[bytes, None] = None,
        ) -> str:

    work_factors = quacks.configs['hashing']['work_factors']
    hashing_function = getattr(hashlib, quacks.configs['hashing']['algorithm'])

    result_hash: bytes = password.encode()
    for _ in range(work_factors):
        result_hash: bytes = hashing_function(
            result_hash + (salt if salt else b'')
        ).hexdigest().encode()

    return result_hash.decode()


