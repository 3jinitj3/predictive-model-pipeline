from pwdlib import PasswordHash
from configparser_crypt import ConfigParserCrypt

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain: str, hash: str) -> bool:
    return password_hash.verify(plain, hash)

