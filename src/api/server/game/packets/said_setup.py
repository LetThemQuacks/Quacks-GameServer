from api.server.server import WebSocketServer
from ...client import WebSocketClient

from src.api.bigboy.integrity import BigBoy

from .handler import PacketHandler, PacketsPhases
from src.database.errors import CryptoErrors

from src.api.utilities import APIUtils

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
        WebSocketServer.INSTANCE.send_server_info(client)
    else:
        logging.warning(f'{client.addr} failed the SAID check, something suspicious is going on: {intact_response}')
        client.send(APIUtils.error('said', CryptoErrors.INTEGRITY_CHECK_FAILED))
        client.ws.close()

