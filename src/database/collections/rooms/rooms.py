from pymongo.collection import Collection
from typing import Union, Tuple

from ..rooms.utilities import RoomsDBUtils
from ...security.hashing import hash_password

import quacks
import functools
import secrets

class RoomsCollection:
    INSTANCE : 'RoomsCollection'

    def __init__(self, base_collection: Collection) -> None:
        if getattr(RoomsCollection, 'INSTANCE', None):
            raise RuntimeError('RoomsCollection is a singletone object.')
        RoomsCollection.INSTANCE = self
        self.collection = base_collection

    def create_room(self,
                    name: str,
                    password: Union[str, None] = None,
                    max_joins: Union[int, None] = None) -> Tuple[str, dict]:
        """
            Creates a room in the database and returns its ID

            :Parameters:
            - `name`: the room name
            - `password`: NoneType if the room doesn't require a password
            - `max_joins`: NoneType if there isn't a limit of users
        """

        room_id = RoomsDBUtils.generate_unique_id(self.collection)

        mongodb_data = self._setup_room_data(room_id, name, password, max_joins)

        self.collection.insert_one(mongodb_data)

        return room_id + str(bool(password).real), mongodb_data

    def _setup_room_data(self, room_id: str, name: str, password: Union[str, None], max_joins: Union[int, None]) -> dict:
        mongodb_data =  {
            'name': name,
            'custom_id': room_id
        }

        if quacks.configs['hashing']['salt']['enable'] and password:
            salt = secrets.token_urlsafe(quacks.configs['hashing']['salt']['length']).encode()
        else:
            salt = None

        RoomsDBUtils.insert_if_necessary(mongodb_data, 'password', password, process_function=functools.partial(hash_password, salt=salt))
        RoomsDBUtils.insert_if_necessary(mongodb_data, 'salt', salt)
        RoomsDBUtils.insert_if_necessary(mongodb_data, 'max_joins', max_joins)

        return mongodb_data


    def list_rooms(self,
                    filter_search: dict = {
                        '_id': 0                        
                    }) -> list:

        return list(self.collection.find({}, filter_search))

