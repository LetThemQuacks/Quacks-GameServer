from pymongo.collection import Collection
from typing import Union, Tuple
import functools
import hmac

from src.database.collections.rooms.utilities import RoomsDBUtils
from src.database.security.hashing import hash_password
from src.database.errors import RoomsErrors

class RoomsCollection:
    INSTANCE = None

    def __init__(self, base_collection: Collection) -> None:
        if RoomsCollection.INSTANCE:
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

        mongodb_data =  {
            'name': name,
            'custom_id': room_id,
            'online_users': []
        }

        RoomsDBUtils.insert_if_necessary(mongodb_data, 'password', password, process_function=hash_password)
        RoomsDBUtils.insert_if_necessary(mongodb_data, 'max_joins', max_joins)

        self.collection.insert_one(mongodb_data)

        return room_id + str(bool(password).real), mongodb_data

    def _room_exists(self,
                    room_id: str,
                    search_filter: dict = {
                        '_id': 0,
                        'name': 1,
                        'custom_id': 1,
                        'password': 1,
                        'max_joins': 1,
                        'online_users': 1
                    }
                ) -> Union[None, dict]:
        """
            Helper function for join_room()
            Checks if a room exists and returns its data
        """
        return self.collection.find_one({'custom_id': room_id}, search_filter)
    
    def join_room(self,
                  room_id: str,
                  user_id: str,
                  password: Union[str, None]
                ) -> Union[int, dict]:

        room_data: Union[None, dict] = self._room_exists(room_id)
        if not room_data:
            return RoomsErrors.ROOM_NOT_FOUND

        if room_data.get('max_join') and len(room_data['online_users']) > room_data['max_joins']:
            return RoomsErrors.ROOM_LIMIT_REACHED

        if room_data.get('password') and password and not hmac.compare_digest(hash_password(password), room_data['password']):
            return RoomsErrors.INCORRECT_PASSWORD


        self.collection.update_one({'custom_id': room_id}, {
            '$push': {
                'online_users': user_id
            }
        })

        return room_data

    def list_rooms(self,
                    filter_search: dict = {
                        '_id': 0,
                        'pwd': 0
                    }) -> list:

        return self.collection.find({}, filter_search)
