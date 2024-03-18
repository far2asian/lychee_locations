import requests
import json
from bs4 import BeautifulSoup

def download() -> None:
    url = "https://www.lycheegold.com.au/melbourne"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('tbody')
    array = []
    for rows in results.find_all('tr'):
        shop = rows.select('td')[0].get_text(strip=True)
        # print(shop)
        street = rows.select('td')[1].get_text(strip=True)
        # print(street)
        suburb = rows.select('td')[2].get_text(strip=True)
        # print(suburb)
        postcode = rows.select('td')[3].get_text(strip=True)
        # print(postcode)
        array.append({ 'shop':shop, 'street':street, 'suburb':suburb, 'postcode': postcode })

    with open("melbourne.json", "w") as f:
        json.dump(array, f)

def main() -> None:
    download()

if __name__ == '__main__':
    main()
