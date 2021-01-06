import os
import argparse
import requests
import csv

from green import parser as green_parser
from e_dostavka import parser as e_parser
from models import Product
from progress.bar import Bar

request_green = requests.Session()
request_evroopt  = requests.Session()

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
    green_parser.authorize(request_green)

def get_products_csv() -> list:
    products = []
    with open('products.csv', newline='') as csvfile:
        products_csv = csv.DictReader(csvfile)
        for product in products_csv:
            products.append({
                'group' : product['Groupname'],
                'link-e' : product['Link-e'],
                'link-g' : product['Link-g'],
            })
    return products

def create_product(parser, link, group):
    product_info = parser.get_product_info(request_evroopt, link)
    Product.create(
        shop=product_info.get('shop'),
        link=link,
        group = group,
    )

def load_products():
    products = get_products_csv()
    bar = Bar('Load products', max=len(products))
    for product in products:
        try:
            create_product(e_parser, product.get('link-e'), product.get('group'))
            create_product(green_parser, product.get('link-g'), product.get('group'))
        except AttributeError:
            with open('logging.log', 'a') as f:
                f.write(f'Product {product.get("group")} was not found\n')
        bar.next()
    bar.finish()
    

# if arg.update:
#     update_session()

if __name__ == "__main__":
    if not Product.select().count():
        load_products()
    