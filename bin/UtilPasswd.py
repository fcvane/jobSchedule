# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Time    : 2018/7/30 16:16
# # @Author  : Fcvane
# # @Param   : 初始化加密和解密函数
# # @File    : UtilPasswd.py
#
# import base64
# import sys
# from Crypto import Random
# from Crypto.Cipher import AES
#
# bs = AES.block_size
# pad = lambda s: s + (bs - (len(s) % bs)) * chr(bs - len(s) % bs)
# unpad = lambda s: s[:-ord(s[len(s) - 1:])]
#
# # 加密函数
# def encrypt(decryptPassword):
#     paddedPassword = pad(decryptPassword)
#     iv = Random.new().read(AES.block_size)
#     key = Random.new().read(16)
#     cipher = AES.new(key, AES.MODE_CBC, iv)
#     encryptedPassword = base64.b64encode(iv + cipher.encrypt(paddedPassword) + key)
#     return encryptedPassword
#
# # 解密函数
# def decrypt(encryptedPassword):
#     base64Decoded = base64.b64decode(encryptedPassword)
#     iv = base64Decoded[:16]
#     key = base64Decoded[-16:]
#     cipher = AES.new(key, AES.MODE_CBC, iv)
#     plainPassword = unpad(cipher.decrypt(base64Decoded[:-16]))[16:]
#     return plainPassword
#
#
# if __name__ == '__main__':
#     #print (sys.argv)
#     #print (len(sys.argv))
#
#     if len(sys.argv) == 3:
#         if sys.argv[1] == '-e':
#             print (encrypt(sys.argv[2]))
#         elif sys.argv[1] == '-d':
#             print (decrypt(sys.argv[2]))
