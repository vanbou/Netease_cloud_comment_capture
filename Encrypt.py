import base64
import json
import os
from binascii import hexlify

from Crypto.Cipher import AES

second_param = "010001"
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
forth_param = "0CoJUm6Qyw8W8jud"

# 加密解密
class Encrypted():
    '''传入歌曲的ID，加密生成'params'、'encSecKey 返回'''
    def __init__(self):
        self.pub_key = second_param
        self.modulus = third_param
        self.nonce = forth_param

    def create_secret_key(self,  size):
        return hexlify(os.urandom(size))[:16].decode('utf-8')

    def aes_encrypt(self, text,  key):
        iv = '0102030405060708'
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(key.encode('utf-8'),  AES.MODE_CBC,  iv.encode('utf-8'))
        result = encryptor.encrypt(text.encode('utf-8'))
        result_str = base64.b64encode(result).decode('utf-8')
        return result_str

    def rsa_encrpt(self, text,  pubKey,  modulus):
        text = text[::-1]
        rs = pow(int(hexlify(text.encode('utf-8')),  16),  int(pubKey,  16),  int(modulus,  16))
        return format(rs,  'x').zfill(256)

    def search(self, text):
        text = json.dumps(text)
        i = self.create_secret_key(16)
        encText = self.aes_encrypt(text,  self.nonce)
        encText = self.aes_encrypt(encText,  i)
        encSecKey = self.rsa_encrpt(i,  self.pub_key,  self.modulus)
        data = {'params': encText,  'encSecKey': encSecKey}
        return data