import hashlib

# Python program to find SHA256 hexadecimal hash string of a file
import hashlib
import os


f = open("text.txt","wb")

with open("text.txt","rb") as f:
    bytes = f.read() # read entire file as bytes
    readable_hash = hashlib.md5(bytes).hexdigest()
    print(readable_hash)

from pathlib import Path

for path in Path('.').iterdir():
    info = path.stat()
    print(info)



