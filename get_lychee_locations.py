import requests
import json
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd
from jinja2 import Environment, FileSystemLoader

def download() -> None:
    url = "https://www.lycheegold.com.au/melbourne"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('tbody')
    array = []
    for rows in results.find_all('tr'):
        shop = rows.select('td')[0].get_text(strip=True)
        street = rows.select('td')[1].get_text(strip=True)
        suburb = rows.select('td')[2].get_text(strip=True)
        postcode = rows.select('td')[3].get_text(strip=True)
        array.append({ 'shop':shop, 'street':street, 'suburb':suburb, 'postcode': postcode })

    sorted_list = sorted(array, key=lambda d:d['suburb'])

    with open("melbourne.json", "w") as f:
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

def create_table() -> None:
    d = {}
    with open('melbourne.json') as f:
        d = json.load(f)

    df = pd.DataFrame(data=d)
    # df.style.set_properties(**{'text-align': 'left'}).set_table_styles([ dict(selector='thead', props=[('text-align', 'left')] ) ])

    with open('locations.html', 'w') as f:
        f.write(df.to_html(index=False, table_id='myTable'))

def render() -> None:
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("template.html")
    with open('locations.html') as f:
        data = f.read()
        content = template.render(table=data)
        with open('melbourne.html', 'w') as m:
            m.write(content)

def getL(address: str) -> dict:
    safe_string = urllib.parse.quote_plus(address)
    url = f'https://nominatim.openstreetmap.org/search?q={safe_string}&format=json&polygon=1&addressdetails=1'
    page = requests.get(url)
    results = json.loads(page.content)

    return({"lat":results[0]["lat"], "lon":results[0]["lon"]})

def main() -> None:
    # download()
    create_table()
    render()

if __name__ == '__main__':
    main()
