import os

blockchain_dir = os.curdir + '/blocks/'  # get directory of blocks


def get_files():
    files = os.listdir(blockchain_dir)  # get list files
    block_sort = sorted([int(i) for i in files])  # sort block names to 1,2,3,4....
    return block_sort
