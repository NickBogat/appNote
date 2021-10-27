import uuid
import hashlib


def hash_password(password):
    # uuid исползуется для генерации случайного числа
    return hashlib.sha256(password.encode()).hexdigest()

