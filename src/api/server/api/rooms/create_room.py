from flask import Blueprint, request
from flask import g as session

from core import logging

from src.database.collections.rooms.rooms import RoomsCollection
from src.api.server.game.room import RoomServer
from src.api.server import WebSocketServer

create_room = Blueprint('create_room_bp', __name__)

@create_room.route('/', methods=['POST'])
def create_room_endpoint():
    data = session.data

    logging.info(f'Creating room "{data.get("name")}"')

    
    room_id, room_data = RoomsCollection.INSTANCE.create_room(data.get('name'), data.get('password'), data.get('max_join'))
    WebSocketServer.rooms_instances[room_data['custom_id']] = RoomServer(
            WebSocketServer.INSTANCE.sock,
            room_data=room_data
        )

    return {'room': {'id': room_id, 'name': data.get('name')}}

