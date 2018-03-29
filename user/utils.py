import base64
import hashlib
import hmac
import random
import struct
import time
import requests
import os
import json

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


def verify_user(g_response):
    url = "https://www.google.com/recaptcha/api/siteverify"
    print(os.environ.get('CAPTHA_SECRET', ''))
    payload = "secret=%s&" \
              "response=%s" % (os.environ.get('CAPTHA_SECRET', ''), g_response)
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'postman-token': "c39edcba-7548-847c-0a4f-a0c83af30e74"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    resp = json.loads(response.text)
    if 'success' in resp:
        return resp['success']
    # print(response.text)
