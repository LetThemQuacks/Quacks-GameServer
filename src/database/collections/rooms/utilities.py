from typing import Callable, Union
from pymongo.collection import Collection
from core import logging
import random
import string

class RoomsDBUtils:
    @staticmethod
    def insert_if_necessary(dictionary: dict, key: str, value: Union[str, None], process_function: Union[Callable, None] = None) -> None:
        if value is not None:
            dictionary.update({
                key: (
                    process_function(value) if process_function else value
                )
            })

    @staticmethod
    def generate_unique_id(collection: Collection) -> str:
        ID = None
        for repetitions in range(10):
            ID = RoomsDBUtils._generate_id()
            if not collection.find_one({'custom_id': ID}):
                break
            else:
                logging.warning('ID Busy: {ID}, regenerating...')

        if not ID:
            raise RuntimeError('ID Generation process failed.')

        return ID



    @staticmethod
    def _generate_id():
        """
            Helper method for generate_unique_id()
        """
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
