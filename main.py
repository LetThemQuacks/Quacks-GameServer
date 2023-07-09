from flask import Flask
from dotenv import load_dotenv

from src.database.connection import QuacksDatabase
from src.api.server import WebsocketServer

db = QuacksDatabase()

app = Flask(__name__)

if __name__ == '__main__':
    load_dotenv()
    ws = WebsocketServer(app)

    app.run('0.0.0.0', 5000)
