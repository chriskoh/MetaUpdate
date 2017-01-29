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

    # import data, seperate table rows
    soup = html
    body = soup.find('tbody')
    rows = body.find_all('tr')

    rowcount = 0
    topclasses = []

    for row in rows:
        if rowcount == 0: # get top classes and latest update time from first row 
            cols = row.find_all('td')
            for col in cols:
                data = col.get_text()        
                if data != "":
                    if data[0].isdigit():
                        time = data
                    else:
                        topclasses.append(data)
        else:
            cols = row.find_all('td')
            for col in cols:
                data = col.get_text()
                if data != "":
                    print(data)
 
        rowcount += 1


def main():

    os.system("clear")
    data = data_request()
    parse = parse_data(data)


if __name__ == "__main__":
    main()
