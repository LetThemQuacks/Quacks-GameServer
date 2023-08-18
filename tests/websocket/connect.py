import threading
import websocket
import sys
import json

from crypto_algorithms.AES import AESCipher
from crypto_algorithms.RSA import RSACipher

AES_INSTANCE: AESCipher = None
RSA_INSTANCE: RSACipher = None


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
    global AES_INSTANCE

    print()
    if AES_INSTANCE:
        data = AES_INSTANCE.decrypt(message)
        print(data)
        return

    data = json.loads(message)
    print(data)
    print('PACKET >> ')
    if data['type'] == 'server_aes':
        aes_key = RSA_INSTANCE.decrypt(data['data']['aes_key'])
        print('AES KEY', aes_key)
        AES_INSTANCE = AESCipher(aes_key.decode('utf-8'))
        #ws.send(AES_INSTANCE.encrypt(json.dumps({'type': 'move', 'data': {
        #    'direction': (-1, 0)
        #}})))

        t = threading.Thread(target=custom_packets, args=(ws,))
        t.daemon = True
        t.start()

def on_error(ws, error):
    print(error)
 
def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    global RSA_INSTANCE

    private, public = RSACipher.generateKeys(3072)
    RSA_INSTANCE = RSACipher(private, public)
    data = json.dumps({'type': 'client_rsa', 'data': {
        'rsa_key': public
    }})
    print('*** SENDING')
    print(data)
    ws.send(data)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        room_id = sys.argv[-1]
        print(f'* Using room ID {room_id} from args')
    else:
        room_id = input('Please enter a room ID: ')

    print(f'Connecting to ws://127.0.0.1:5000/room?id={room_id}')
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(f"ws://127.0.0.1:5000/room?id={room_id}",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly


