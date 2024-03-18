import requests
import json
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd
from jinja2 import Environment, FileSystemLoader

def download(city: str) -> None:
    url = f"https://www.lycheegold.com.au/{city}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('tbody')
    array = []
    for rows in results.find_all('tr'):
        shop = rows.select('td')[0].get_text(strip=True)
        street = rows.select('td')[1].get_text(strip=True)
        suburb = rows.select('td')[2].get_text(strip=True)
        if len(suburb) == 0:
            continue
        array.append({ 'shop':shop, 'street':street, 'suburb':suburb})

    sorted_list = sorted(array, key=lambda d:d['suburb'])

    with open(f"{city}.json", "w") as f:
        json.dump(sorted_list, f)

    # Was going to use OSM to get latitude and longitude but their address database is limited and doesn't provide the right
    # co-ordinates for a given address, only for the road4
    #
    #   
    # with open("melbourne.txt", "w") as txt_file:
    #     for sample in sorted_list:
    #         txt_file.write(f'{sample["shop"]}\t{sample["street"]}\t{sample["suburb"]}\n')
    #
    # print(getL(f'{sample["street"]}, {sample["suburb"]}'))

def create_table(city: str) -> None:
    d = {}
    with open(f"{city}.json") as f:
        d = json.load(f)

    df = pd.DataFrame(data=d)

    with open(f"{city}_locations.html", 'w') as f:
        f.write(df.to_html(index=False, table_id='myTable'))

def render(city: str) -> None:
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("template.html")
    with open(f"{city}_locations.html") as f:
        data = f.read()
        content = template.render(table=data, city=city.capitalize())
        with open(f"{city}.html", 'w') as m:
            m.write(content)

def getL(address: str) -> dict:
    safe_string = urllib.parse.quote_plus(address)
    url = f'https://nominatim.openstreetmap.org/search?q={safe_string}&format=json&polygon=1&addressdetails=1'
    page = requests.get(url)
    results = json.loads(page.content)

    return({"lat":results[0]["lat"], "lon":results[0]["lon"]})

def main() -> None:
    cities = [
        "melbourne",
        "sydney-1",
        "canberra-and-south-coast",
        "brisbane",
        "adelaide"
    ]
    for city in cities:
        download(city)
        create_table(city)
        render(city)

if __name__ == '__main__':
    main()
