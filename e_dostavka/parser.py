import bs4
import requests
import json
import os

from bs4 import BeautifulSoup as BS


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
}

STATUS_OK = 200
SHOP = "e-dostavka"
request = requests.Session()

def get_product_page(request, url) -> BS:
    page = ""
    try:
        r = request.get(url, headers=HEADERS)
        assert (r.status_code == STATUS_OK), "Check your URL or internet connection"
        page = BS(r.text, 'html.parser')
    except AssertionError as Assert:
        print(Assert)
    return page


def get_price(product: bs4.BeautifulSoup) -> float:
    with open("index.html", 'w') as f:
        f.write(product.prettify())
    try:
        price = float(
            product.find('div', class_='products_card')
            .find('meta',itemprop="price").get('content')
        )
    except TypeError:
        price = 0
    return price


def get_name(product: bs4.BeautifulSoup) -> str:
    try:
        name = product.find('h1').text
    except AttributeError:
        name = ""
    return name


def is_authorised(product: bs4.BeautifulSoup) -> bool:
    authorised = False
    try:
        if not product.find("a", class_="link_enter"):
            authorised = True
    except TypeError:
        pass
    return authorised


def get_product_info(request, url: str)-> dict:
    product = get_product_page(request, url)
    data = {}

    data["price"] = get_price(product)
    data["name"] = get_name(product)
    data["is_authorise"] = is_authorised(product)
    data["shop"] = SHOP
    return data


def authorize(request):
    if not os.path.exists("e-dostavla/config.json"):
        try:
            with open("e-dostavka/auth.json", "r") as read_file:
                auth_data = json.load(read_file)
        except FileNotFoundError:
            return request
        token_response = request.post('https://rest.eurotorg.by/10201/Json?What=GetJWT', json=auth_data).json()
        with open("e-dostavka/config.json", "w") as write_file:
            write_file.write(json.dumps(token_response))
    else:
        with open("e-dostavka/config.json", "r") as read_file:
            token_response = json.load(read_file)
    request.get(f'https://e-dostavka.by/cabinet/enter/?token={token_response["Table"][0]["JWT"]}&return=/')

# print(get_product_info(request, 'https://e-dostavka.by/catalog/item_1058157.html'))
# print(get_product_info(request, 'https://e-dostavka.by/catalog/item_1005900.html'))

# authorize(request)

# print(get_product_info(request, 'https://e-dostavka.by/catalog/item_1058157.html'))