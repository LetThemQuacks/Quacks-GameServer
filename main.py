from flask import Flask
from flask_sock import Sock
from dotenv import load_dotenv

from src.database.connection import QuacksDatabase

db = QuacksDatabase()

app = Flask(__name__)
sock = Sock()

if __name__ == '__main__':
    load_dotenv()

    sock.init_app(app)
    app.run('0.0.0.0', 5000)
