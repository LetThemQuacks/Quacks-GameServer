from flask import Flask, cli, redirect
from quacks import Quacks
from configs import configs
from core import ACTIVE_SERVER

cli.show_server_banner = lambda *args, **kwargs: None

app = Flask(__name__)
Quacks(app)

@app.route('/')
def home():
    return redirect(ACTIVE_SERVER)

if __name__ == '__main__':
    app.run(configs['hosting']['address'], configs['hosting']['port'])
