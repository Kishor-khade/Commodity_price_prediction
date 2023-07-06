import html
from bs4 import BeautifulSoup
import json

with open('Scraper/Bike_Scrape/Bike_dekho/BikeDekho_places.html') as f:
    page_html_list = f.readlines()
    page_html_str = ''.join(page_html_list)

# print(page_html_str)
soup = BeautifulSoup(page_html_str, "lxml")
# print(soup.prettify())
# def places_list():
#     places = soup.text
#     places = places.split('\n')
#     # places = places[2:]

#     places = [i.rstrip().lstrip() for i in places[2:] if i != '']
#     return places
# print(soup.find_all('data-gs-ta-val["slug"]'))

# soup = BeautifulSoup(html_doc, 'html.parser')

def places_list():
    places = []
    for li in soup.find_all('li')[1:]:
        data = li.attrs['data-gs-ta-val']
        data = json.loads(data)
        # print(data)
        places.append(data['slug'])

    return places[:]
# print(places_list())
    