from page_scraper import Scraper
from page import Page
from product import Product
import json
from db import MySQL
import db_creation_script

DB_CONFIG_FILE = "db/db_config.json"
DB_NAME = "aliexpress"


def read_json(path):
    """Returns a data from json"""
    try:
        with open(path) as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        raise Exception(f"Error: No such file: {path}")


def main():
    # NOTE: url and categories are hardcoded, but will be replaced in the future.
    """
    Gets products from 1st page and inserts them into database
    """
    
    url = "https://www.aliexpress.com/category/708042/cpus.html?spm=a2g0o.home.104.5.650c2145wzJtZH"
    category = 0

    config = read_json(DB_CONFIG_FILE)
    db = MySQL(config)
    db_creation_script.start()
    
    scraper = Scraper(silent_mode=False)
    # Set language, country and currency
    scraper.apply_page_settings(url)
    # NOTE: silent_mode must be set to False !!! Don't close the browser
    # scraper.apply_page_settings(url)

    # Debugging

    page = Page(scraper.get_page(url))

    
    db.push(f"USE {DB_NAME};")
    for url in page.get_links():
        url = 'https://' + url
        print(url)
        product = Product(url, scraper.get_page(url))
        print(f'{product.id}, {product.link}, {product.title}, {product.rating}, {product.n_reviews}, {product.n_orders}, {product.price}, {category}')
        db.push(f'INSERT INTO products (id, link, title, rating, n_reviews, n_orders, price, category_id)\
            VALUES ({product.id}, "{product.link}", "{product.title}", {product.rating}, {product.n_reviews}, {product.n_orders}, {product.price}, {category});')

if __name__ == "__main__":
    main()
