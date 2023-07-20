import os
import logging as logging_module
from dotenv import load_dotenv
from rich.logging import RichHandler

load_dotenv()

level = logging_module.getLevelName(os.getenv('LOG_LEVEL', 'INFO'))

logging_module.basicConfig(
    level=level,
    format= '%(message)s',
    datefmt='%H:%M:%S',
    handlers=[RichHandler(markup=True)]
)

# DO NOT change this if you don't know what you are doing.
MAIN_SERVER: str = 'https://quacks-website.vercel.app'

logging = logging_module.getLogger('rich')

