import json
import os
import requests
from bs4 import BeautifulSoup
from modules.get_files import get_files
from modules.get_hash import get_hash

currency = []
price = []
page = requests.get('https://cbr.ru/key-indicators/')
soup = BeautifulSoup(page.text, "lxml")  # parser

blockchain_dir = os.curdir + '/blocks/'  # get directory of blocks


def parse_course():
    if page.status_code == 200:
        currency_find = soup.find_all('div', {'class': 'd-flex title-subinfo'})
        price_find = soup.find_all('td', class_='value td-w-4 _bold _end mono-num')
        for curr in currency_find:
            currency_sort = curr.find('div', {'class': 'col-md-5'}).text.strip()
            currency.append(currency_sort)
        for i in price_find:
            price.append(i.get_text())
    #    print_course()

    # def print_course():
    #    diction = dict(zip(currency, price))
    #    for key in diction:
    #        print('Курс', key, 'на сегодня:', diction[key])
    else:
        print(f'Error: {page.status_code}')


def check_integrity():
    block_sort = get_files()
    results = []
    #  check block for rewriting, begin - the second block, the first block is genesis
    for file in block_sort[1:]:
        f = open(blockchain_dir + str(file))  # open block
        hash_block = json.load(f)['hash']  # hook a hash from data
        prev_block = str(file - 1)
        actual_hash = get_hash(prev_block)  # get previous block hash

        if hash_block == actual_hash:  # check hashes
            result = 'ok'
        else:
            result = 'not ok'
        results.append({'block': prev_block, 'result': result})
    return results


def write_block(currency, price, prev_hash=''):
    block_sort = get_files()
    last_block = block_sort[-1]  # get last block
    filename = str(last_block + 1)

    prev_hash = get_hash(str(last_block))  # get previous hash of block (function get_hash)

    # blocks data
    data = {'currency': currency,
            'price': price,
            'hash': prev_hash}

    # write data to block in json format
    with open(blockchain_dir + filename, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)  # indent = 4 as comfortable for read

    # count blocks and write to file number of blocks
    with open('count_blocks.txt', 'w') as file_2:
        files = os.listdir(path=blockchain_dir)
        file_2.write(str(len(files)))


def main():
    parse_course()
    diction = dict(zip(currency, price))
    for key in diction:
        write_block(currency=key, price=diction[key], prev_hash='')
    print(check_integrity())


if __name__ == '__main__':
    main()
