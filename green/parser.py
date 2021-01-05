from http.cookiejar import Cookie
import requests
import json
import os
import re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
}

STATUS_OK = 200 
SHOP = "green"

request = requests.Session()
store_id = 2

def get_product_info(request, url, store_id) -> dict:
    data = {}
    try:
        response = request.get(f'{url}?storeId={store_id}', headers=HEADERS)
        assert (response.status_code == STATUS_OK), "Check your URL or internet connection"
        data = response.json()
    except AssertionError as Assert:
        print(Assert)
    return data

def get_name(data:json) -> str:
    title = ''
    try:
        title = data['title']
    except (KeyError, TypeError):
        pass
    return title

def get_price(data:json) -> float:
    price = 0.0
    try:
        price = float(data['storeProduct']['priceWithSale'])/100
    except (KeyError, TypeError):
        pass
    return price

# def is_authorised(request) -> bool:
#     if request.cookies

def get_product(request, url: str)-> dict:
    product = {}
    data = get_product_info(request, url, store_id)
    product["price"] = get_price(data)
    product["name"] = get_name(data)
    product["is_authorise"] = True if 'Authorization' in request.cookies.keys() else False
    product["shop"] = SHOP
    
    return product

def authorize(request):
    phone_number = ""
    if not os.path.exists('green/config.json'):
        while(True):
            phone_number = input("Enter you phone number (+375XXXXXXXXX): ")
            if re.match(r"^\+375([29|44|25|33]{2})(\d{7})$", phone_number):
                break
            else:
                print("Try again and in correct format")
        request.post('https://shop.green-market.by/api/v1/auth/request-confirm-code/', json={"phoneNumber" : phone_number})
        response = request.post('https://shop.green-market.by/api/v1/auth/verify-confirm-code/', json={"phoneNumber": phone_number, "code" : input("Enter your code: ")})

        with open("green/config.json", "w") as write_file:
            write_file.write(json.dumps(response.cookies._cookies['shop.green-market.by']['/']['Authorization'].__dict__))
    else:
        with open("green/config.json", "r") as read_file:
            cookie = json.load(read_file)
        request.cookies.set_cookie(Cookie(*cookie.values()))


# https://shop.green-market.by/api/v1/products/4570232
print(get_product(request, 'https://shop.green-market.by/api/v1/products/4317'))
authorize(request)
print(get_product(request, 'https://shop.green-market.by/api/v1/products/4317'))