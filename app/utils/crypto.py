import random
import string
import hashlib


def get_random_string(length: int) -> str:
    # choose from all lowercase letter
    characters = string.ascii_letters + string.digits

    return ''.join(random.choice(characters) for i in range(length))


def hash_string(raw: str) -> str:
    s = hashlib.sha1()

    s.update(raw.encode('utf8'))
    return s.hexdigest()
