from page_scraper import Scraper
from page import Page
from product import Product
from db import MySQL
import db_creation_script
from global_functions import read_json
from global_variables import Constants


def main():
    # NOTE: url and categories are hardcoded, but will be replaced in the future.
    """
    Gets products from 1st page and inserts them into database
    """

    url = "https://www.aliexpress.com/category/708042/cpus.html"
    category = 0

    config = read_json(Constants.DB_CONFIG_FILE)
    db = MySQL(config)
    db_creation_script.start(mode="skip")

    scraper = Scraper(silent_mode=False)
    # Set language, country and currency
    scraper.apply_page_settings(url)
    # NOTE: silent_mode must be set to False !!! Don't close the browser

    page = Page(scraper.get_page(url))

    db.push(f"USE {Constants.DB_NAME};")
    for url in page.get_links():
        url = "https://" + url
        print(url)
        product = Product(url, scraper.get_page(url))
        print(
            f"{product.id}, {product.link}, {product.title}, {product.rating}, {product.n_reviews}, {product.n_orders}, {product.price}, {category}"
        )
        db.push(
            f'REPLACE INTO products (id, link, title, rating, n_reviews, n_orders, price, category_id)\
            VALUES ({product.id}, "{product.link}", "{product.title}", {product.rating}, {product.n_reviews}, {product.n_orders}, {product.price}, {category});'
        )


if __name__ == "__main__":
    main()
