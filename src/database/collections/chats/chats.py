import time
from bson.objectid import ObjectId
from pymongo.collection import Collection

class ChatsCollection:
    INSTANCE : 'ChatsCollection'

    def __init__(self, base_collection: Collection) -> None:
        if getattr(ChatsCollection, 'INSTANCE', None):
            raise RuntimeError('RoomsCollection is a singletone object.')
        ChatsCollection.INSTANCE = self
        self.collection = base_collection

    def create_chat(self) -> ObjectId:
        return self.collection.insert_one({
            'messages': [],
            'authors': {}
        }).inserted_id

    def add_message(self, chat: ObjectId, msg_data: dict) -> None:
        self.collection.update_one({'_id': chat},
                                   {'$push': {'messages': {'$each': [msg_data], '$position': 0}}}
        )

    def add_user(self, chat, client):
        self.collection.update_one({'_id': chat}, {'$set': {f'authors.{client.user_id}': {
            'username': client.username,
            'skin': client.skin,
            'color': client.color
        }}})

    def get_messages(self, chat_id: ObjectId, start: int = 0, end: float = float('inf')):
        chat = self.collection.find_one({'_id': chat_id}) 
        if not chat:
            raise RuntimeError(f'Chat not found: {chat_id}')

        if end == float('inf'):
            end = len(chat['messages'])
        
        end = int(end)

        return chat['messages'][start:end]

    def get_authors(self, chat_id: ObjectId):
        chat = self.collection.find_one({'_id': chat_id}) 
        if not chat:
            raise RuntimeError(f'Chat not found: {chat_id}')

        return chat['authors']

