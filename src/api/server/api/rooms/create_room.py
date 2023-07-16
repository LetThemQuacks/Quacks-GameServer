from flask import Blueprint, request
from flask import g as session

from src.database.collections.rooms.rooms import RoomsCollection
from src.api.server.game.room import RoomServer
from src.api.server import WebSocketServer

create_room = Blueprint('create_room_bp', __name__)

@create_room.route('/', methods=['POST'])
def create_room_endpoint():
    data = session.data
    
    room_id, room_data = RoomsCollection.INSTANCE.create_room(data.get('name'), data.get('password'), data.get('max_join'))
    WebSocketServer.rooms_instances[room_id[:-1]] = RoomServer(
            WebSocketServer.INSTANCE.sock,
            room_id=room_id,
            room_data=room_data
        )

    return {'room': {'id': room_id, 'name': data.get('name')}}

