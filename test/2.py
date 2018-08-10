#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/31 14:21
# @Author  : Fcvane
# @Param   : 
# @File    : 2.py
from Crypto.Cipher import AES
from Crypto import Random
import base64

bs = AES.block_size
pad = lambda s: s + (bs - (len(s) % bs)) * chr(bs - len(s) % bs)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, rawdata):
        rawdata = pad(rawdata)
        iv = Random.new().read(AES.block_size)
        #key = Random.new().read(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encryptedPassword = base64.b64encode(iv + cipher.encrypt(rawdata) + self.key)
        #return (iv + cipher.encrypt(rawdata))
        return encryptedPassword

    def decrypt(self, enc):
        iv = enc[:bs]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]))


def main():
    key = Random.new().read(16)
    cipher = AESCipher(key)

    msg = 'abc123'
    encrypted = cipher.encrypt(msg)
    print ('encrypted data: ', encrypted)

    decrypted = cipher.decrypt(encrypted)
    print ('decrypted data: ', decrypted)


if __name__ == '__main__':
    main()