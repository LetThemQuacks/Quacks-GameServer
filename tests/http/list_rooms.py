import requests
from rich import print_json

res = requests.get(
    'http://127.0.0.1:5000/rooms/',
)
print_json(res.text)
