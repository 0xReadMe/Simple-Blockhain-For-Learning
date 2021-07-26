import hashlib
import os

blockchain_dir = os.curdir + '/blocks/'  # get directory of blocks


def get_hash(filename):
    file = open(blockchain_dir + filename, 'rb').read()  # open block for read
    return hashlib.md5(file).hexdigest()  # return hash of block
