import websocket
import _thread
import time
import rel
import sys
import json

from crypto_algorithms.AES import AESCipher
from crypto_algorithms.RSA import RSACipher

AES_INSTANCE: AESCipher = None
RSA_INSTANCE: RSACipher = None

def on_message(ws, message):
    global AES_INSTANCE

    print('*** RECEIVED')
    if AES_INSTANCE:
        data = AES_INSTANCE.decrypt(message)
        print(data)
        return

    data = json.loads(message)
    print(data)
    if data['t'] == 'server_aes':
        aes_key = RSA_INSTANCE.decrypt(data['d']['aes_key'])
        print('AES KEY', aes_key)
        AES_INSTANCE = AESCipher(aes_key.decode('utf-8'))
        ws.send(AES_INSTANCE.encrypt(json.dumps({'t': 'move', 'd': {
            'direction': (-1, 0)
        }})))

def on_error(ws, error):
    print(error)
 
def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    global RSA_INSTANCE

    private, public = RSACipher.generateKeys(3072)
    RSA_INSTANCE = RSACipher(private, public)
    data = json.dumps({'t': 'client_rsa', 'd': {
        'rsa_key': public
    }})
    print('*** SENDING')
    print(data)
    ws.send(data)

if __name__ == "__main__":
    room_id = sys.argv[-1]
    print(f'Connecting to ws://127.0.0.1:50000/room?id={room_id}')
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(f"ws://127.0.0.1:5000/room?id={room_id}",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
