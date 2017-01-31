#!/usr/bin/env python3

import requests
import os
from operator import itemgetter
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
    topdecks = []
    matchups = []
    results = {}

    for row in rows:

        rates = []
        deck = ""
        tempresults = {}

        if rowcount == 0: # get top classes and latest update time from first row 
            cols = row.find_all('td')
            for col in cols:
                data = col.get_text()        
                if data != "":
                    if data[0].isdigit():
                        time = data
                    else:
                        topdecks.append(data)
        else: # get deck matchups from remaining rows
            cols = row.find_all('td')
            for col in cols:
                data = col.get_text()
                if data:
                    if data[0].isdigit():
                        rates.append(data)
                    else:
                        deck = data

        # sort data in to dict
        if len(topdecks) == len(rates):
            
            for x in range(0,len(topdecks)):
                tempresults[topdecks[x]] = rates[x]
            results[deck] = tempresults
        rowcount += 1

    return results

def calculate(results):

    keys = results.keys()

    freq = sorted(results['Frequency'].items(), key=itemgetter(1))
    freq.reverse()

    rec = {}
    for key in freq:
        if key[0] != "Win Rate":
            rec[key[0]] = 0

    # Display current deck encounter frequency / matchups
    print("Current Meta \n")
    print("Encounters: (Encouter Rate% @ Win Ratio%)\n")
    for key in freq:
        if key[0] != "Win Rate":
            wr = float(results[key[0]]['Win Rate']) * 100
            er = float(key[1]) * 100
            print("    " + key[0] + ": " + "{0:.2f}".format(round(er,2)) + "% @ " + "{0:.2f}".format(round(wr,2)) + "%")

    print("\nMatchups")
    for key in freq:
        if key[0] != "Win Rate":
            print("\n    " + key[0])
            matchups = sorted(results[key[0]].items(), key=itemgetter(1))
            matchups.reverse()
            for match in matchups:
                if match[0] != "Win Rate":
                    wr = float(match[1]) * 100
                    print("        " + match[0] + ": " + "{0:.2f}".format(round(wr,2)) + "%")
                    if ((float(match[1]) * 100) < 50):
                        rec[match[0]] += 1

    suggested = sorted(rec.items(), key=itemgetter(1))
    suggested.reverse()
    print("\nSuggested decks (Based on number of favorable matchups):")
    for key in suggested:
        print("    " + key[0] + ": " + str(key[1]))


def main():

    os.system("clear")
    data = data_request()
    parse = parse_data(data)
    calculate(parse)

if __name__ == "__main__":
    main()
