import os
import string
import random
import binascii
import hashlib
from ecdsa import BadSignatureError
from ecdsa.curves import SECP256k1
from ecdsa.der import UnexpectedDER
from ecdsa.keys import VerifyingKey
from ecdsa.util import sigdecode_der

from app.constants import PIN_LENGTH


def is_staff(user):
    is_editor = user.groups.filter(name='editor').exists()
    return (is_editor or user.is_superuser)


def verify_signature(message, public_key, signature):
    public_key = uncompress_ecdsa_public_key(public_key)
    verifying_key = VerifyingKey.from_string(unhexlify(public_key), SECP256k1, hashlib.sha256)
    try:
        verifying_key.verify(unhexlify(signature), message.encode(), hashlib.sha256, sigdecode_der)
    except (BadSignatureError, UnexpectedDER):
        return False
    return True


def unhexlify(data):
    if len(data) % 2:
        data = "0" + data
    result = binascii.unhexlify(data)
    return result


def uncompress_ecdsa_public_key(pubkey):
    """
    https://bitcointalk.org/index.php?topic=644919.msg7205689#msg7205689
    """
    p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
    y_parity = int(pubkey[:2]) - 2
    x = int(pubkey[2:], 16)
    a = (pow(x, 3, p) + 7) % p
    y = pow(a, (p + 1) // 4, p)
    if y % 2 != y_parity:
        y = -y % p
    return '{:x}{:x}'.format(x, y)


def generate_pin():
    characters = []
    for _ in range(PIN_LENGTH):
        rand = random.SystemRandom().choice(string.ascii_letters + string.digits)
        characters.append(rand)
    return ''.join(characters)
