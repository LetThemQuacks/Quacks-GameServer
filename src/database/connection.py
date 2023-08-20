from pymongo import MongoClient
from pymongo.database import Database

from dotenv import load_dotenv
from core import logging
from configs import configs

from src.database.collections.rooms.rooms import RoomsCollection

import os

load_dotenv()

class QuacksDatabase:
    DEFAULT_COLLECTIONS: list = ['rooms']
    rooms: RoomsCollection

    def __init__(self) -> None:
        logging.info('Connecting to the MongoDB Database...')
        self.connection = MongoClient(os.getenv('CONNECTION_URL'))
        self.init_database()
    
    def init_database(self) -> None:
        """
            Initialize the DataBase
        """

        logging.info('Initializing DataBase')

        self.database: Database = self.connection[configs['database']['db_name']]
        self.init_collections()



    def init_collections(self) -> bool:
        """
            Returns True if any collection has been created.
        """

        logging.info('Initializing Collections')

        existing_collections: list = self.database.list_collection_names()
        track: bool = False

        logging.debug(f'Existing Collections: {existing_collections}')

        for collection in self.DEFAULT_COLLECTIONS:
            logging.debug(f'Checking if collection "{collection}" exists')
            if not collection in existing_collections:
                track = True
                self.database.create_collection(collection, check_exists=False)
                logging.info(f'Collection "{collection}" has been created')

        self.rooms = RoomsCollection(self.database.rooms)

        return track
