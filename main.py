from flask import Flask, cli, redirect
from quacks import Quacks
from core import ACTIVE_SERVER

cli.show_server_banner = lambda *args, **kwargs: None

app = Flask(__name__)
Quacks(app)

@app.route('/')
def home():
    return redirect(ACTIVE_SERVER)

if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
