import os
from cryptography.fernet import Fernet

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
        print('secret key already exist!')
        print('Abort...')
        return

    print(f'Generating secret key at {KEY_LOCATION}')
    try:
        key = Fernet.generate_key()
        with open(KEY_LOCATION, 'wb') as f:
            f.write(key)
    except Exception as e:
        print(e)
        print('Some error occurred at generating key')
        print('Abort...')
    print('secret key was created successfully!')


def load_key() -> bytes:
    """Load key

    Returns:
        bytes: byte data from secret key
    """
    if not key_exists():
        generate_key()

    key = None
    with open(KEY_LOCATION, 'rb') as f:
        key = f.read()
    return key


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


def decrypt(encrypted_text: bytes) -> str:
    """Decrypt encrypted text

    Args:
        encrypted_text (str): encrypted text

    Returns:
        str: decrypted text
    """
    f = Fernet(load_key())
    decrypted_text = f.decrypt(encrypted_text).decode()

    return decrypted_text


if __name__ == '__main__':
    generate_key()
