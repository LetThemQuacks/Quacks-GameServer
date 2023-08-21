from ...client import WebSocketClient

from ....bigboy.integrity import BigBoy

from .handler import PacketHandler, PacketsPhases
from .....database.errors import CryptoErrors

from ....utilities import APIUtils

from json import dumps
from core import logging

@PacketHandler.handle(packet_type='said', working_phase=PacketsPhases.PRE_SAID)
def check_client_server_access_id(client: WebSocketClient, data: dict) -> None:
    integrity_data = client.INTEGRITY.copy()
    integrity_data.update({'said': data['said']})

    logging.debug(f'Checking if the SAID [cyan]{data["said"][:25]}...[/] is valid')
    intact_response = BigBoy.check_aes_and_rsa_integrity(**integrity_data)
    is_intact = intact_response['ok']
    logging.debug(f'SAID Valid Check: {is_intact}')

    integrity_data.update({'intact': is_intact})

    if is_intact:
        client.INTEGRITY = integrity_data
        client.phase = PacketsPhases.OPERATIONAL
        client.setup_user_info(**intact_response['profile'])
    else:
        logging.warning(f'{client.addr} failed the SAID check, something suspicious is going on')
        client.send(dumps(APIUtils.error('said', CryptoErrors.INTEGRITY_CHECK_FAILED)))
        client.ws.close()

