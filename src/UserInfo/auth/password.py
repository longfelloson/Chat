import hashlib


def get_hashed_password(plain_password: str) -> str:
    """
    Gets hashed password for given plain password.
    """
    return hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
