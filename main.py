from page_scraper import Scraper
from page import Page
from product import Product
from db import MySQL
import db_creation_script
from global_functions import read_json
from global_variables import Constants
import time



def print_log(log, bracket='='):
    """Prints the log in an easy-to-read format"""
    bracket_multiplier = len(log)
    print('\n', bracket * bracket_multiplier, sep='')
    print(log)
    print(bracket * bracket_multiplier, '\n', sep='')


def main():

    """
    Gets products from 1st page and inserts them into database
    """
    
    main_start_time = time.time()
    print_log(f"Main function started: {time.asctime(time.localtime(main_start_time))}")
    

    # NOTE: url and categories are hardcoded, but will be replaced in the future.
    url = "https://www.aliexpress.com/category/708042/cpus.html"
    category = 0

    # Database initialization
    db = MySQL(read_json(Constants.DB_CONFIG_FILE))
    db_creation_script.start(mode="force")
    db.push(f"USE {Constants.DB_NAME};")

    # Scraper initialization
    scraper_initialization_start_time = time.time()
    print_log(f"Scraper initialization started: {time.asctime(time.localtime(scraper_initialization_start_time))}")
    scraper = Scraper(silent_mode=True, scroll_pause_time=1)
    scraper.get_page(Constants.ROOT_URL)
    scraper.add_cookies(read_json(Constants.COOKIES_FILE))
    print_log(f"Scraper initialization ended in: {round(time.time() - scraper_initialization_start_time, 2)} seconds")


    page = Page(scraper.get_page(url))

    db.push(f"USE {Constants.DB_NAME};")
    item = 0
    start_time = time.time()
    print_log(f"Scraping from page started: {time.asctime(time.localtime(start_time))}")
    
    for url in page.get_links():
        try:
            product = Product(url, scraper.get_page(url))
            db.push(
                f'REPLACE INTO products (id, link, title, rating, n_reviews, n_orders, price, category_id)\
                VALUES ({product.id}, "{product.link}", "{product.title}", {product.rating}, {product.n_reviews}, {product.n_orders}, {product.price}, {category});'
            )
            item += 1
            print(f"Product #{item} - id: {product.id}")
        except Exception as e:
            print(f"Unable to process product. URL: {url}\nError: {e}")
    
    print_log(f"Scraping from page ended in: {round(time.time() - start_time, 2)} seconds")

    
    print_log(f'Main function ended in: {round(time.time() - main_start_time, 2)} seconds')
    print_log(f'{time.asctime(time.localtime(time.time()))}')


if __name__ == "__main__":
    main()
