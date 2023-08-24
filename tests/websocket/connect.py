import threading
import websocket
import sys
import json
import time
import requests

#from rich import print

from crypto_algorithms.AES import AESCipher
from crypto_algorithms.RSA import RSACipher

AES_INSTANCE: AESCipher = None
RSA_INSTANCE: RSACipher = None
public_rsa = None


BIG_BOY_API = 'https://quacks-nightly.vercel.app/api'

def custom_packets(ws):
    while True:
        data = input('PACKET >> ')
        if data.startswith('raw:'):
            ws.send(data[4:])
        elif data.startswith('join:'):
            ws.send(AES_INSTANCE.encrypt(json.dumps({'type': 'join_room', 'data': {'id': data[5:]}})))
        elif data.startswith('msg:'):
            ws.send(AES_INSTANCE.encrypt(json.dumps({'type': 'send_message', 'data': {'message': data[4:]}})))
        else:
            ws.send(AES_INSTANCE.encrypt(data))

def on_message(ws, message):
    global AES_INSTANCE, public_rsa


    if AES_INSTANCE:
        data = AES_INSTANCE.decrypt(message)
        print('crypted:', data)
        return

    data = json.loads(message)
    print('raw:', message)
    sys.stdout.write("\033[F")
    if data['type'] == 'server_aes':
        aes_key = RSA_INSTANCE.decrypt(data['data']['aes_key'])

        print(public_rsa)

        response = requests.post(
            BIG_BOY_API + '/said/new',
            json = {
                'aes': aes_key.decode('utf-8'),
                'rsa': public_rsa
            },
            cookies={
                'session': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7InVzZXJuYW1lIjoiVHJhcGEiLCJfaWQiOiI2NDQxYWU3MTA3NmE5NTE1MDlmMDJmNjYifSwiaWF0IjoxNjkyNjM3MTQzLCJleHAiOjE2OTI3MjM1NDN9.Q3LxcMsr6HKzeibW7LjzDTF1ef8CSlZ_uWkgFKuLEt4'
            }
        ).json()
        print(response)
        said = response['said']
        
        said_packet = {
            'type': 'said',
            'data': {
                'said': said
            }
        }

        AES_INSTANCE = AESCipher(aes_key.decode('utf-8'))

        print(f'send: {json.dumps(said_packet)}')
        ws.send(AES_INSTANCE.encrypt(json.dumps(said_packet)))

        t = threading.Thread(target=custom_packets, args=(ws,))
        t.daemon = True
        t.start()
    else:
        print(data)

def on_error(ws, error):
    print(error)
 
def on_close(ws, close_status_code, close_msg):
    print("\n[red]########## WEBSOCKET CLOSED ##########[/]")
    print(f'{close_status_code = }')
    print(f'{close_msg = }')

def on_open(ws):
    global RSA_INSTANCE, public_rsa

    t = time.time()
    private, public = RSACipher.generateKeys(1354)
    print(f'RSA key generation took {time.time() - t} seconds')
    public_rsa = public
    RSA_INSTANCE = RSACipher(private, public)
    print(public)
    data = json.dumps({'type': 'client_rsa', 'data': {
        'rsa_key': public
    }})
    ws.send(data)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        room_id = sys.argv[-1]
        print(f'* Using room ID {room_id} from args')
    else:
        room_id = 'null'

    print(f'Connecting to ws://127.0.0.1:5000/room?id={room_id}')
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(f"ws://127.0.0.1:5000/room?id={room_id}",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly


