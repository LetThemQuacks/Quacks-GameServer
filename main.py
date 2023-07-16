from flask import Flask
from quacks import Quacks

app = Flask(__name__)

if __name__ == '__main__':
    Quacks(app)
    app.run('0.0.0.0', 5000)
