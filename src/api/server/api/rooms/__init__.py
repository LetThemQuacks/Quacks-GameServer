from flask import Blueprint

from .create_room import create_room
from .list_rooms  import list_rooms

rooms = Blueprint('rooms_blueprint', __name__, url_prefix='/rooms')
rooms.register_blueprint(create_room)
rooms.register_blueprint(list_rooms)

