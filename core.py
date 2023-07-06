import os
import logging
from dotenv import load_dotenv

load_dotenv()

level = logging.getLevelName(os.getenv('LOG_LEVEL', 'INFO'))

logging.basicConfig(
    level=level,
    format= '[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

# DO NOT change this if you don't know what you are doing.
MAIN_SERVER: str = 'https://quacks-website.vercel.app'

