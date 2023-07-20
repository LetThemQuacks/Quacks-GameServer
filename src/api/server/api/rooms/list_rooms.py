from flask import Blueprint, request
from flask import g as session
from src.database.collections.rooms.rooms import RoomsCollection

list_rooms = Blueprint('list_room_bp', __name__)

@list_rooms.route('/', methods=['GET'])
def list_rooms_endpoint():
    room_list = RoomsCollection.INSTANCE.list_rooms()
    return {'rooms': room_list}
