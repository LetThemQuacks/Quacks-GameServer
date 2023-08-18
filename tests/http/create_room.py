import requests
import sys

res = requests.post(
    'http://127.0.0.1:5000/rooms/',
    json = {
        "name": sys.argv[-1],
        "max_joins": 3,
        "password": "SuperSecretPassword"
    }
)
print(res.text)
