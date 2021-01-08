import os
import argparse
import requests
import csv

from green import parser as green_parser
from e_dostavka import parser as e_parser
from models import Product, Price, conn
from progress.bar import Bar
from datetime import date


def parsargument():
    parser = argparse.ArgumentParser(description='Parser of shop.green and e-dostavka products')
    parser.add_argument(
        '--update',
        action='store_true',
        help="update session in shop green.by"
    )
    parser.add_argument(
        '--compare',
        choices=range(2, 8),
        type=int,
        help="Compare for the last N days"
    )
    return parser.parse_args()


arg = parsargument()


def update_session():
    if (os.path.exists('green/config.json')):
        os.remove('green/config.json')
    green_parser.authorize(requests.Session())


def get_products_csv() -> list:
    products = []
    with open('products.csv', newline='', encoding='utf-8') as csvfile:
        products_csv = csv.DictReader(csvfile)
        for product in products_csv:
            products.append({
                'group' : product['Groupname'],
                'link-e' : product['Link-e'],
                'link-g' : product['Link-g'],
            })
    return products


def load_products():
    products = get_products_csv()
    bar = Bar('Load products', max=len(products))
    for product in products:
        Product.create(
            link_e=product.get('link-e'),
            link_g=product.get('link-g'),
            group = product.get('group'),
        )
        bar.next()
    bar.finish()
    

def main_parser(parser, request, id, link):
    product_info = parser.get_product_info(request, link)
    Price.create(date=date(2021, 1, 7), price=product_info.get('price'), product_id=id, authorized=product_info.get('is_authorise'), shop=product_info.get('shop'))


def parse_price():
    request_green = requests.Session()
    request_evroopt = requests.Session()

    authorized_request_green = green_parser.authorize(requests.Session())
    authorized_request_evroopt = e_parser.authorize(requests.Session())

    if date(2021, 1, 7) in [price.date for price in Price.select().execute()]:
        return
    else:
        products = Product.select().order_by(Product.id).execute()
        bar = Bar('Parse prices', max=len(products))
        
        for product in products:
            with conn.atomic() as trn:
                try:
                    main_parser(green_parser, request_green, product.id, product.link_g)
                    main_parser(green_parser, authorized_request_green, product.id, product.link_g)
                    main_parser(e_parser, request_evroopt, product.id, product.link_e)
                    main_parser(e_parser, authorized_request_evroopt, product.id, product.link_e)
                except AttributeError:
                    trn.rollback()
                finally:
                    bar.next()
        bar.finish()


# def get_prices()


def compare(days_count : int):
    # TODO делать парсер всегда ровно в 00:00
    days = [day.date for day in Price.select().distinct(Price.date)]
    
    if days_count >= len(days):
        print(f"Parser has only {len(days)} day(s) info")
        return
    elif days_count <= 0:
        print(f"Error with days_count <= 0")
        return
    else:
        for product in Product.select().execute():
            today_prices = Price.select().where((Price.date == date.today()) & (Price.product == product.id)).execute()
            past_prices = Price.select().where((Price.date == days[-days_count-1]) & (Price.product == product.id)).execute()
            # print(today_prices)
            print('-------')
            for prices in zip(today_prices, past_prices):
                print(prices[0].date, prices[0].authorized, prices[0].price, prices[0].shop)
                print(prices[1].date, prices[1].authorized, prices[1].price, prices[1].shop)
            
    # pass


if __name__ == "__main__":
    if arg.update:
        update_session()
        exit(0)
    if not Product.select().count():
        load_products()
    parse_price()
    compare(1)
