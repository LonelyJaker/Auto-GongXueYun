from utils import AES


def Encrypt(key, text):
    a = AES(key.encode("utf-8"))
    res = a.encrypt(text.encode('utf-8'))
    msg = res.hex()
    return msg
