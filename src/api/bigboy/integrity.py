import json
import urllib.request

from core import ACTIVE_SERVER, logging

class BigBoy:
    # SAID: Server Accedd ID
    @staticmethod
    def check_aes_and_rsa_integrity(aes: str, rsa: str, said: str, **kwargs) -> dict:
        request = urllib.request.Request(ACTIVE_SERVER + '/api/said/integrity', 
            data=json.dumps({
                'rsa': rsa,
                'aes': aes,
                'said': said
            }).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        try:
            response = urllib.request.urlopen(request)
        except Exception as e:
            print(e)
            return {'ok': False}

        try:
            data = json.loads(response.read().decode('utf-8'))
        except Exception:
            logging.exception('Failed to parse BigBoy response from /api/integrity')
            logging.critical('BigBoy integrity check has failed')
            return {'ok': False}

        return data
