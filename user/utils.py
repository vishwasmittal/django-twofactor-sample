import base64
import hashlib
import hmac
import random
import struct
import time


def get_hotp_token(secret, intervals_no):
    key = base64.b32decode(secret)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[19] & 15
    h = (struct.unpack(">I", h[o:o + 4])[0] & 0x7fffffff) % 1000000
    return h


def get_totp_token(secret):
    return get_hotp_token(secret, intervals_no=int(time.time()) // 30)


def generate_secret(length=16):
    random_secret = ""
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    for _ in range(length):
        random_secret += random.choice(characters)
    return random_secret


def confirm_totp_token(token, secret):
    tokens = [get_hotp_token(secret, intervals_no=(int(time.time()) // 30) - 1),
              get_hotp_token(secret, intervals_no=int(time.time()) // 30),
              get_hotp_token(secret, intervals_no=(int(time.time()) // 30)) + 1]
    # print(tokens)
    if token in tokens:
        return True
    else:
        return False
