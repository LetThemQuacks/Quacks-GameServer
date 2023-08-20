import requests

from core import ACTIVE_SERVER, logging

class BigBoy:
    # SAID: Server Accedd ID
    @staticmethod
    def check_aes_and_rsa_integrity(aes: str, rsa: str, said: str, **kwargs) -> dict:
        response = requests.post(ACTIVE_SERVER + '/said/integrity', json={
            'rsa': rsa,
            'aes': aes,
            'said': said
        })
        
        try:
            response = response.json()
        except Exception:
            logging.exception('Failed to parse BigBoy response from /api/integrity')
            logging.critical('BigBoy integrity check has failed')
            return {'ok': False}

        return response
