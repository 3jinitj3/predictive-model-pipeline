from dotenv import load_dotenv
import os
from configparser_crypt import ConfigParserCrypt

load_dotenv()

JWT_KEY_FILE = os.getenv('JWT_KEY_FILE')
ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('JWT_EXPIRATION_MINUTES', '30'))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv('JWT_REFRESH_EXPIRATION_DAYS', '30'))
with open(JWT_KEY_FILE, 'r') as key_file:
    if not JWT_KEY_FILE:
        raise RuntimeError('JWT_KEY_FILE environment variable not configured.')
    JWT_SECRET = key_file.read().strip()

DB_KEY = os.getenv('DB_KEY')
DB_INI = os.getenv('DB_INI')
DB_ENCRYPTED_INI = os.getenv('DB_ENCRYPTED_INI')

def db_conf_encryption():
    original_file = DB_INI
    target_encrypted_file = DB_ENCRYPTED_INI

    conf = ConfigParserCrypt()
    conf.generate_key(32)
    aes_key = conf.aes_key
    with open(DB_KEY, 'wb') as k:
        k.write(aes_key)

    conf.read(original_file)
    with open(target_encrypted_file, 'wb') as encrypted_path:
        conf.write_encrypted(encrypted_path)
