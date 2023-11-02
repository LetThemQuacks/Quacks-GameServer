from bson.objectid import ObjectId
from pymongo.collection import Collection
from typing import Union, Tuple

from ..rooms.utilities import RoomsDBUtils
from ...security.hashing import hash_password

from configs import configs
import functools
import secrets

class RoomsCollection:
    INSTANCE : 'RoomsCollection'

    def __init__(self, base_collection: Collection) -> None:
        if getattr(RoomsCollection, 'INSTANCE', None):
            raise RuntimeError('RoomsCollection is a singletone object.')
        RoomsCollection.INSTANCE = self
        self.collection = base_collection

        # Parsing Configs Dictionary
        self.hashing_enabled = configs['hashing']['salt']['enable']

    def create_room(self,
                    name: str,
                    password: Union[str, None] = None,
                    max_joins: Union[int, None] = None,
                    chat_id: Union[ObjectId, None] = None) -> Tuple[str, dict]:
        """
            Creates a room in the database and returns its ID

            :Parameters:
            - `name`: the room name
            - `password`: NoneType if the room doesn't require a password
            - `max_joins`: NoneType if there isn't a limit of users
        """

        room_id = RoomsDBUtils.generate_unique_id(self.collection)

        mongodb_data = self._setup_room_data(room_id, name, password, max_joins, chat_id)

        self.collection.insert_one(mongodb_data)

        return room_id + str(bool(password).real), mongodb_data

    def _setup_room_data(self, room_id: str, name: str, password: Union[str, None], max_joins: Union[int, None], chat_id: Union[ObjectId, None], is_password_hash: bool = False) -> dict:
        mongodb_data =  {
            'name': name,
            'custom_id': room_id,
        }

        pwd_salt = self._generate_pwd_salt() if (self.hashing_enabled and password) else None
        pwd_process_function = functools.partial(hash_password, salt=pwd_salt) if not is_password_hash else None

        RoomsDBUtils.insert_if_necessary(mongodb_data, 'password', password, process_function=pwd_process_function)
        RoomsDBUtils.insert_if_necessary(mongodb_data, 'salt', pwd_salt)
        RoomsDBUtils.insert_if_necessary(mongodb_data, 'max_joins', max_joins)
        RoomsDBUtils.insert_if_necessary(mongodb_data, 'chat', chat_id)

        return mongodb_data

    def _generate_pwd_salt(self):
        return secrets.token_urlsafe(configs['hashing']['salt']['length']).encode()

    def list_rooms(self,
                    filter_search: dict = {
                        '_id': 0                        
                    }) -> list:

        return list(self.collection.find({}, filter_search))

    def delete_room(self, room_id: str):
        return self.collection.delete_one({'custom_id': room_id})
