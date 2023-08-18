import os
import logging as logging_module
from dotenv import load_dotenv
from rich.logging import RichHandler

load_dotenv()

# Official API Servers configuration (aka BigBoy)
# DO NOT change this if you don't know what you are doing.
__MAIN_SERVER: str = 'https://quacks-website.vercel.app'
__DEVELOPMENT_SERVER: str = 'https://quacks-nightly.vercel.app'

ACTIVE_SERVER = __DEVELOPMENT_SERVER

# Logging Setup
level = logging_module.getLevelName(os.getenv('LOG_LEVEL', 'INFO'))

logging_module.basicConfig(
    level=level,
    format= '%(message)s',
    datefmt='%H:%M:%S',
    handlers=[RichHandler(markup=True)]
)

logging = logging_module.getLogger('rich')

del __MAIN_SERVER, __DEVELOPMENT_SERVER
