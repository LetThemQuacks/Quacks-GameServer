import math
import uuid
import numpy

# Local (no-socket) client-server implementation.

class Duck:
    velocity = numpy.array([0.0, 0.0])
    position = numpy.array([0.0, 0.0])

class Server:
    def __init__(self):
        self.ducks = {}

    def add_duck(self, duck: Duck):
        ID = str(uuid.uuid4())
        self.ducks[ID] = duck
        return ID

    def verify_direction(self, direction):
        return 

    def set_direction(self, ID, direction):
        pass

server = Server()

duck = Duck()
server.add_duck(duck)


