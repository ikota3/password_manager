import os
from cryptography.fernet import Fernet


# secret.key location(at password_manager/secret.key)
KEY_LOCATION = os.path.normpath(os.path.join(os.path.dirname(__file__), '../secret.key'))


def key_exists() -> bool:
    """Check key exists

    Returns:
        bool: True if key exists, otherwise False
    """
    return os.path.isfile(KEY_LOCATION)


def generate_key() -> None:
    """Generate secret key
    """
    if key_exists():
        print('Secret key already exist.')
        print('Abort...')
        return

    print(f'Generating secret key at {KEY_LOCATION}.')
    key = Fernet.generate_key()
    try:
        with open(KEY_LOCATION, 'wb') as f:
            f.write(key)
    except IOError as e:
        print('Failed to generate secret key.')
        print(e)
        raise
    print('Secret key was successfully generated.')


def load_key() -> bytes:
    """Load key

    Returns:
        bytes: byte data from secret key
    """
    if not key_exists():
        try:
            generate_key()
        except BaseException:
            return

    key = None
    try:
        with open(KEY_LOCATION, 'rb') as f:
            key = f.read()
        return key
    except IOError as e:
        print('Failed to load secret key.')
        print(e)


def encrypt(plain_text: str) -> bytes:
    """Encrypt plain text

    Args:
        plain_text (str): plain text

    Returns:
        str: encrypted text
    """
    f = Fernet(load_key())
    encrypted_text = f.encrypt(plain_text.encode())

    return encrypted_text


def decrypt(encrypted_bytes: bytes) -> str:
    """Decrypt encrypted bytes

    Args:
        encrypted_bytes (bytes): encrypted bytes

    Returns:
        str: decrypted text
    """
    f = Fernet(load_key())
    decrypted_text = f.decrypt(encrypted_bytes).decode()

    return decrypted_text
