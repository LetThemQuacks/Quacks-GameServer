from flask import Flask, cli
from quacks import Quacks
import os

cli.show_server_banner = lambda *args, **kwargs: None

app = Flask(__name__)
Quacks(app)

if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
