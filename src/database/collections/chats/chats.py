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
            'messages': []
        }).inserted_id

    def add_message(self, chat: ObjectId, msg_id: str, author_id: str, author_name: str, content: str) -> None:
        self.collection.update_one({'_id': chat}, {'$push': {'messages': {
            'id': msg_id,
            'content': content,
            'timestamp': time.time(),
            'author': {
                'name': author_name,
                'id': author_id
            }
        }}})

    def get_messages(self, chat_id: ObjectId, start: int = 0, end: float = float('inf')):
        chat = self.collection.find_one({'_id': chat_id}) 

        if end == float('inf'):
            end = len(chat['messages'])
        
        end = int(end)

        return chat['messages'][start:end]
