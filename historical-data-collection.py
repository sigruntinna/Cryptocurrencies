import requests
from bs4 import BeautifulSoup as bs
import csv
from itertools import chain

"""historical-data-collection.py: This python script scrapes historical data
from http://coinmarketcap.com and puts it in *cryptocurrency*.csv"""

__author__ = [
    "Sigrún Tinna Gissurardóttir",
    "Unnur Sól Ingimarsdóttir"
]

def scrape(urls):
    all_dicts = []

    for url in urls:
        cryptocurrency_list = []

        cryptocurrency_page = requests.get(url)
        cryptocurrency_soup = bs(cryptocurrency_page.content, "html.parser")

        for col in cryptocurrency_soup.find("div", {"id": "historical-data"}).find("table").find("tr").find_all("th"):
            cryptocurrency_list.append(str(col.string).strip())

        for row in cryptocurrency_soup.find("div", {"id": "historical-data"}).find("table").find_all("tr"):
            value_list = []

            for value in row.find_all("td"):
                value_list.append(str(value.string).strip())

            if value_list:
                cryptocurrency_dict = dict(zip(cryptocurrency_list, value_list))
                all_dicts.append(cryptocurrency_dict)

    return all_dicts

def save_csv(list_of_dicts):
    with open("neo.csv", "w", newline='') as csv_file:
        fieldnames = list(set(key for key in chain(*list_of_dicts)))
        fieldnames = sorted(fieldnames, key=lambda x: x == "Date", reverse = True)

        writer = csv.DictWriter(csv_file, fieldnames)
        writer.writeheader()
        writer.writerows(list_of_dicts)

if __name__ == "__main__":
    bitcoin_url = ["https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20160101&end=20171231"]
    ethereum_url = ["https://coinmarketcap.com/currencies/ethereum/historical-data/?start=20160101&end=20171231"]
    ripple_url = ["https://coinmarketcap.com/currencies/ripple/historical-data/?start=20160101&end=20171231"]
    litecoin_url = ["https://coinmarketcap.com/currencies/litecoin/historical-data/?start=20160101&end=20171231"]
    neo_url = ["https://coinmarketcap.com/currencies/neo/historical-data/?start=20160101&end=20171231"]
    save_csv(scrape(neo_url))
