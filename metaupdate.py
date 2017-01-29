#!/usr/bin/env python3

import requests
import os
from bs4 import BeautifulSoup

# request Vicious Syndicate data (updated hourly)
def data_request():

    set_url = "https://docs.google.com/spreadsheets/d/1osCVci8-7ttXp_CjWORzEUYf5VQlGWN_ZsOUrbCX0AI/pubhtml/sheet?headers=false&gid=344714981"
    meta_response = requests.get(set_url)
    meta_data = meta_response.text
    data = BeautifulSoup(meta_data, "lxml")

    return data

# parse Vicious Syndicate data
def parse_data(html):
    soup = html

    rows = soup.find_all('tr')
    for row in rows:
        print('------')
        print(row) 

def main():

    os.system("clear")
    data = data_request()
    parse = parse_data(data)


if __name__ == "__main__":
    main()
