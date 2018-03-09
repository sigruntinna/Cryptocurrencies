import requests
from bs4 import BeautifulSoup as bs
import csv
from itertools import chain

"""data-collection.py: This python script scrapes results from political election
from http://www.kosningastofnun.in and puts it in votes.csv"""

__author__ = "Sigrún Tinna Gissurardóttir"

def get_urls():
    page = requests.get("http://www.kosningastofnun.in/")
    page_soup = bs(page.content, "html.parser")

    urls = [article.find("a").get("href") for article in page_soup.find(class_ = "blog-main").find_all("article")]

    return urls

def scrape(urls):
    all_dicts = []

    for url in urls:
        political_list = []

        political_page = requests.get(url)
        political_soup = bs(political_page.content, "html.parser")

        for party in political_soup.find("table").find("tr").find_all("th"):
            political_list.append(str(party.string).strip())

        for row in political_soup.find("table").find_all("tr"):
            vote_list = []

            for vote in row.find_all("td"):
                vote_list.append(str(vote.string).strip())

            if vote_list:
                # If the date was not in the table, then we
                # find it in the header of the article
                if "Dagsetning" not in political_list:
                    political_list.append("Dagsetning")
                    vote_list.append(find_date(political_soup))

                political_dict = dict(zip(political_list, vote_list))
                all_dicts.append(political_dict)

    return all_dicts

def find_date(political_soup):
    return " ".join((str(political_soup.find("h2").find("a").string).split())[1:])

def save_csv(list_of_dicts):
    with open("votes-with-all-dates.csv", "w", newline='') as csv_file:
        fieldnames = list(set(key for key in chain(*list_of_dicts)))
        fieldnames = sorted(fieldnames, key=lambda x: x == "Dagsetning", reverse = True)

        writer = csv.DictWriter(csv_file, fieldnames)
        writer.writeheader()
        writer.writerows(list_of_dicts)

if __name__ == "__main__":
    save_csv(scrape(get_urls()))
